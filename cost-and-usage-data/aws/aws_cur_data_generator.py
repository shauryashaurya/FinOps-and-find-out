import pandas as pd
import numpy as np
import random
import uuid
import datetime
import multiprocessing
import os
import json
from collections import defaultdict
import calendar
import hashlib
import time
from tqdm import tqdm

# Import configuration
from aws_config import CONFIG

# Set random seed for reproducibility
# the answer to life, universe and everything (#DOUGADAMS, IYKYK)
np.random.seed(42)
random.seed(42)

# Constants and helper variables
START_DATE = datetime.date.today(
) - datetime.timedelta(days=CONFIG["number_of_days"])
END_DATE = datetime.date.today()
CURRENCY_CODE = "USD"
LINE_ITEM_TYPES = ["Usage", "Tax", "DiscountedUsage",
                   "SavingsPlanCoveredUsage", "Credit"]
LINE_ITEM_TYPE_WEIGHTS = [0.8, 0.05, 0.05, 0.07, 0.03]  # Probability weights
INVOICE_PREFIX = "I-"

# Data volume reduction settings - adjust these to control the amount of data generated
DATA_VOLUME_SETTINGS = {
    # number of projects to generate data for, originally specified to be 7
    "maximum_projects_to_be_picked": 11,
    "days_to_generate": 512,     # Number of days to generate data for
    "sampling_interval": 3,     # Generate data every X days
    "max_services_per_project": 9,  # Limit number of services per project
    "max_resources_per_service": 3,  # Number of resources per service
    "max_usage_records_per_day": 4,  # Max usage records per day per resource
    "primary_regions_per_project": 1,  # Number of primary regions
    "dr_region_probability": 0.2,     # Probability of using DR region
    "volatility_factor": 0.02,        # +/- 2% cost volatility by default
}

# Tag categories for more realistic tagging
TAG_CATEGORIES = {
    "Technical": [
        {"key": "Name", "values": None},  # Will be set dynamically
        {"key": "Environment", "values": [
            "Production", "Development", "Testing", "Staging", "QA", "UAT", "DR"]},
        {"key": "Version", "values": [
            "1.0", "2.0", "3.0", "latest", "stable", "beta"]},
        {"key": "AutoShutdown", "values": [
            "true", "false", "weekends", "nights"]},
        {"key": "BackupFrequency", "values": [
            "daily", "hourly", "weekly", "monthly", "none"]},
        {"key": "DataClassification", "values": [
            "public", "internal", "confidential", "restricted"]},
    ],
    "Business": [
        {"key": "Project", "values": None},  # Will be set from project name
        # Will be set from project data
        {"key": "BusinessUnit", "values": None},
        {"key": "CostCenter", "values": None},  # Will be generated dynamically
        {"key": "Department", "values": [
            "IT", "Engineering", "Finance", "Marketing", "Sales", "Research", "Operations"]},
        {"key": "Owner", "values": ["john.doe@example.com", "jane.smith@example.com", "team-devops@example.com",
                                    "sre-team@example.com", "cloud-admin@example.com"]},
        {"key": "Requestor", "values": ["john.doe@example.com", "jane.smith@example.com", "team-devops@example.com",
                                        "product-team@example.com", "project-manager@example.com"]},
    ],
    "Compliance": [
        {"key": "Compliance:HIPAA", "values": ["required", "not-required"]},
        {"key": "Compliance:PCI", "values": ["in-scope", "out-of-scope"]},
        {"key": "Compliance:SOX", "values": ["in-scope", "out-of-scope"]},
        {"key": "Compliance:GDPR", "values": ["in-scope", "out-of-scope"]},
        {"key": "SecurityLevel", "values": [
            "low", "medium", "high", "critical"]},
        {"key": "ComplianceStatus", "values": [
            "compliant", "non-compliant", "exempted", "under-review"]},
    ],
    "Automation": [
        {"key": "CreatedBy", "values": [
            "Terraform", "CloudFormation", "Ansible", "Console", "CLI", "SDK"]},
        {"key": "ManagedBy", "values": [
            "CloudOps", "DevOps", "SRE", "Platform", "Manual"]},
        {"key": "IaC", "values": ["true", "false"]},
        {"key": "AutoScaling", "values": ["enabled", "disabled"]},
        {"key": "DeploymentGroup", "values": [
            "blue", "green", "canary", "main", "experiment"]},
    ],
    "FinOps": [
        {"key": "AllowSpotInstance", "values": ["true", "false"]},
        {"key": "OptimizationPriority", "values": [
            "cost", "performance", "availability", "balanced"]},
        {"key": "BudgetAlert", "values": ["low", "medium", "high", "exempt"]},
        {"key": "ScheduledDowntime", "values": [
            "weekends", "nights", "never", "custom"]},
        {"key": "Rightsizing", "values": [
            "optimized", "pending-review", "oversized", "exempt"]},
    ]
}

# Service-specific tags
SERVICE_SPECIFIC_TAGS = {
    "EC2": [
        {"key": "InstanceType", "values": None},  # Will be set dynamically
        {"key": "AMI", "values": ["ami-12345678",
                                  "ami-87654321", "ami-custom", "ami-approved"]},
        {"key": "AutoShutdown", "values": [
            "true", "false", "weekends", "nights"]},
        {"key": "PatchGroup", "values": [
            "group1", "group2", "critical", "standard", "dev"]},
    ],
    "S3": [
        {"key": "StorageClass", "values": [
            "Standard", "IntelligentTiering", "StandardIA", "OneZoneIA", "Glacier"]},
        {"key": "Encryption", "values": ["AES256", "aws:kms", "none"]},
        {"key": "PublicAccess", "values": [
            "blocked", "allowed-read-only", "controlled"]},
        {"key": "LifecyclePolicy", "values": [
            "30-day-transition", "90-day-archive", "1-year-deletion", "compliance-7-years"]},
    ],
    "RDS": [
        {"key": "Engine", "values": [
            "mysql", "postgres", "aurora", "sqlserver", "oracle"]},
        {"key": "MultiAZ", "values": ["true", "false"]},
        {"key": "BackupRetention", "values": ["7", "14", "30", "90"]},
        {"key": "DBName", "values": ["prod-db",
                                     "dev-db", "test-db", "analytics-db"]},
    ],
    "Lambda": [
        {"key": "Runtime", "values": [
            "python3.9", "nodejs14.x", "java11", "go1.x", "dotnet6"]},
        {"key": "MemorySize", "values": ["128", "256", "512", "1024", "2048"]},
        {"key": "Timeout", "values": ["30", "60", "300", "900"]},
        {"key": "EventSource", "values": [
            "api", "s3", "dynamodb", "sqs", "schedule"]},
    ],
    "DynamoDB": [
        {"key": "TableClass", "values": [
            "Standard", "StandardInfrequentAccess"]},
        {"key": "BillingMode", "values": ["PROVISIONED", "PAY_PER_REQUEST"]},
        {"key": "BackupPlan", "values": [
            "daily", "weekly", "none", "continuous"]},
        {"key": "TTL", "values": ["enabled", "disabled"]},
    ],
    "EBS": [
        {"key": "VolumeType", "values": [
            "gp2", "gp3", "io1", "io2", "st1", "sc1"]},
        {"key": "Encrypted", "values": ["true", "false"]},
        {"key": "SnapshotFrequency", "values": [
            "daily", "weekly", "monthly", "none"]},
        {"key": "DeleteOnTermination", "values": ["true", "false"]},
    ],
}

# Chargeback models for the organization
CHARGEBACK_MODELS = {
    "direct": {
        "description": "Direct chargeback - costs charged directly to consuming departments",
        "allocation_method": "direct"
    },
    "proportional": {
        "description": "Proportional allocation - shared costs distributed based on relative usage",
        "allocation_method": "proportional"
    },
    "equal": {
        "description": "Equal distribution - shared costs split equally",
        "allocation_method": "equal"
    },
    "tiered": {
        "description": "Tiered allocation - different rates based on consumption levels",
        "allocation_method": "tiered"
    }
}

# Cost allocation structures
COST_ALLOCATION_RULES = {
    "shared_services": {
        "model": "proportional",
        # What metric to use for proportional allocation
        "allocation_key": "compute_usage",
        "entities": ["IT", "Finance", "Marketing", "Sales", "Operations", "Engineering"],
        "services": ["VPC", "DirectConnect", "Route53", "CloudWatchLogs", "SecurityHub"]
    },
    "data_services": {
        "model": "direct",
        "allocation_key": "data_volume",
        "entities": ["Analytics", "DataScience", "ProductDevelopment"],
        "services": ["S3", "RDS", "DynamoDB", "Redshift", "Athena", "Glue"]
    },
    "security_compliance": {
        "model": "equal",
        "allocation_key": None,
        "entities": ["IT", "SecurityOperations", "Compliance", "Legal", "Finance"],
        "services": ["GuardDuty", "IAM", "KMS", "WAF", "Config", "SecurityHub"]
    }
}

# Different allocation percentages for shared resources
# For example, a database shared by multiple applications
SHARED_RESOURCE_ALLOCATIONS = {
    "enterprise-data-lake": {
        "Analytics": 0.40,
        "Sales": 0.25,
        "ProductDevelopment": 0.20,
        "Finance": 0.15
    },
    "central-auth-service": {
        "IT": 0.60,
        "SecurityOperations": 0.25,
        "Compliance": 0.15
    }
}

# Reserved Instance benefit mapping for blended/unblended cost simulation
RI_DISCOUNT_MAPPING = {
    "EC2": {
        # Mapping account IDs to discount factors
        # Values <1 indicate discount (account owns RIs)
        # Values >1 indicate paying the premium (account uses shared RIs)
        "111111111111": 0.7,  # Management account with a lot of RIs - gets 30% RI discount
        "555555555555": 0.85,  # Security account - gets 15% RI discount
        "222200000001": 1.05,  # Aviation Dev - pays 5% more
        "444400000001": 0.9,   # Aviation Prod - gets 10% RI discount
    },
    "RDS": {
        "111111111111": 0.75,  # Management account - gets 25% RI discount
        "666666666666": 0.85,  # Shared Services - gets 15% RI discount
        "444400000002": 0.95,  # Pharma Prod - gets 5% RI discount
    }
}

# AWS CUR Schema columns (subset - we'll expand as needed)
CUR_COLUMNS = [
    "identity/LineItemId",
    "identity/TimeInterval",
    "bill/InvoiceId",
    "bill/BillingEntity",
    "bill/BillType",
    "bill/PayerAccountId",
    "bill/BillingPeriodStartDate",
    "bill/BillingPeriodEndDate",
    "lineItem/UsageAccountId",
    "lineItem/LineItemType",
    "lineItem/UsageStartDate",
    "lineItem/UsageEndDate",
    "lineItem/ProductCode",
    "lineItem/UsageType",
    "lineItem/Operation",
    "lineItem/AvailabilityZone",
    "lineItem/ResourceId",
    "lineItem/UsageAmount",
    "lineItem/NormalizationFactor",
    "lineItem/NormalizedUsageAmount",
    "lineItem/CurrencyCode",
    "lineItem/UnblendedRate",
    "lineItem/UnblendedCost",
    "lineItem/BlendedRate",
    "lineItem/BlendedCost",
    "lineItem/LineItemDescription",
    "lineItem/TaxType",
    "product/ProductName",
    "product/servicecode",
    "product/region",
    "pricing/unit",
    "pricing/publicOnDemandCost",
    "pricing/publicOnDemandRate",
    "pricing/term",
    "pricing/offeringClass"
]

# Resource Tags columns
RESOURCE_TAGS_COLUMNS = [
    "resourceId",
    "key",
    "value"
]


def calculate_daily_budget():
    """Calculate daily budget from annual budget"""
    annual_budget = CONFIG["annual_budget"]
    daily_budget = annual_budget / 365.0
    return daily_budget


def get_account_id_for_stage(stage_name):
    """Find account ID for a given stage name from the account hierarchy"""
    def search_hierarchy(node, target_stage):
        if "account_id" in node and target_stage.lower() in node.get("name", "").lower():
            return node["account_id"]

        if "children" in node:
            for child_name, child_node in node["children"].items():
                if target_stage.lower() in child_name.lower() and "account_id" in child_node:
                    return child_node["account_id"]

                result = search_hierarchy(child_node, target_stage)
                if result:
                    return result
        return None

    # Add name field to each node in hierarchy for easier searching
    def add_names(node, name=""):
        node["name"] = name
        if "children" in node:
            for child_name, child_node in node["children"].items():
                add_names(child_node, child_name)

    hierarchy = CONFIG["account_hierarchy"].copy()
    add_names(hierarchy["Organization"], "Organization")

    # First try direct match
    for stage in CONFIG["project_stages"]:
        if stage.lower() == stage_name.lower():
            result = search_hierarchy(hierarchy["Organization"], stage)
            if result:
                return result

    # Try partial match
    result = search_hierarchy(hierarchy["Organization"], stage_name)
    if result:
        return result

    # Default to management account if not found
    return hierarchy["Organization"]["account_id"]


def generate_resource_id(service_name, region, instance_type=None):
    """Generate a realistic AWS resource ID based on service type"""
    if service_name == "EC2":
        return f"i-{uuid.uuid4().hex[:8]}"
    elif service_name == "S3":
        return f"my-{service_name.lower()}-bucket-{uuid.uuid4().hex[:8]}"
    elif service_name == "RDS":
        return f"{service_name.lower()}-instance-{uuid.uuid4().hex[:8]}"
    elif service_name == "Lambda":
        return f"{service_name.lower()}-function-{uuid.uuid4().hex[:12]}"
    elif service_name == "DynamoDB":
        return f"{service_name.lower()}-table-{uuid.uuid4().hex[:8]}"
    elif service_name == "EBS":
        return f"vol-{uuid.uuid4().hex[:8]}"
    elif service_name == "CloudFront":
        return f"distribution-{uuid.uuid4().hex[:8]}"
    else:
        return f"{service_name.lower()}-resource-{uuid.uuid4().hex[:8]}"


def generate_arn(service_name, region, resource_id, account_id):
    """Generate a realistic AWS ARN"""
    service_prefix = service_name.lower()

    # Handle special cases
    if service_name == "EC2":
        if resource_id.startswith("i-"):
            return f"arn:aws:ec2:{region}:{account_id}:instance/{resource_id}"
        elif resource_id.startswith("vol-"):
            return f"arn:aws:ec2:{region}:{account_id}:volume/{resource_id}"
    elif service_name == "S3":
        return f"arn:aws:s3:::{resource_id}"
    elif service_name == "Lambda":
        return f"arn:aws:lambda:{region}:{account_id}:function:{resource_id}"
    elif service_name == "DynamoDB":
        return f"arn:aws:dynamodb:{region}:{account_id}:table/{resource_id}"
    elif service_name == "RDS":
        return f"arn:aws:rds:{region}:{account_id}:db:{resource_id}"

    # Default pattern
    return f"arn:aws:{service_prefix}:{region}:{account_id}:{resource_id}"


def apply_lifecycle_pattern(day_index, total_days, lifecycle, usage_amount_base, volatility=0.02):
    """
    Apply usage pattern based on lifecycle with added volatility for more realistic patterns

    Args:
        day_index: Current day index
        total_days: Total number of days in the simulation
        lifecycle: Project lifecycle pattern
        usage_amount_base: Base usage amount
        volatility: Volatility factor (default: 0.02 or 2%)

    Returns:
        Adjusted usage amount
    """
    configurables = CONFIG["configurables"]
    growth_rate = configurables["usage_growth_rate"].get(lifecycle, 1.0)

    # Base lifecycle pattern calculation
    if lifecycle == "growing":
        # Simply apply growth rate
        base_pattern = usage_amount_base * (growth_rate ** day_index)

    elif lifecycle == "growing_then_sunset":
        sunset_start_day = int(
            total_days * configurables["sunset_start_day_ratio"])
        if day_index < sunset_start_day:
            # Growth phase
            base_pattern = usage_amount_base * (growth_rate ** day_index)
        else:
            # Sunset phase
            growth_at_sunset = usage_amount_base * \
                (growth_rate ** sunset_start_day)
            sunset_days = day_index - sunset_start_day
            base_pattern = growth_at_sunset * \
                (configurables["sunset_decline_rate"] ** sunset_days)

    elif lifecycle == "just_started":
        # Low initial usage with rapid growth
        base_pattern = usage_amount_base * 0.1 * \
            (growth_rate ** (2 * day_index))

    elif lifecycle == "steady_state":
        # Minimal growth/fluctuation
        base_pattern = usage_amount_base * \
            (growth_rate ** day_index) * (0.95 + 0.1 * np.random.random())

    elif lifecycle == "declining":
        # Steady decline
        base_pattern = usage_amount_base * (growth_rate ** day_index)

    elif lifecycle == "peak_and_plateau":
        plateau_start_day = int(
            total_days * configurables["peak_plateau_start_day_ratio"])
        plateau_end_day = plateau_start_day + \
            int(total_days * configurables["peak_plateau_duration_ratio"])

        if day_index < plateau_start_day:
            # Growth to peak
            base_pattern = usage_amount_base * (growth_rate ** day_index)
        elif day_index <= plateau_end_day:
            # Plateau phase
            peak_value = usage_amount_base * (growth_rate ** plateau_start_day)
            # Small fluctuations during plateau
            base_pattern = peak_value * (0.98 + 0.04 * np.random.random())
        else:
            # Slight decline after plateau
            peak_value = usage_amount_base * (growth_rate ** plateau_start_day)
            days_after_plateau = day_index - plateau_end_day
            base_pattern = peak_value * (0.999 ** days_after_plateau)
    else:
        base_pattern = usage_amount_base  # Default

    # Apply volatility - random factor between (1-volatility) and (1+volatility)
    volatility_factor = 1.0 + random.uniform(-volatility, volatility)

    # Apply daily volatility to the base pattern
    result = base_pattern * volatility_factor

    # Weekly pattern - slight uptick on weekdays, decrease on weekends
    current_date = START_DATE + datetime.timedelta(days=day_index)
    day_of_week = current_date.weekday()

    # Apply business hours pattern: more usage on Tuesday-Thursday,
    # less on Monday/Friday, much less on weekends
    if day_of_week == 5 or day_of_week == 6:  # Weekend
        result *= random.uniform(0.7, 0.9)
    elif day_of_week == 0 or day_of_week == 4:  # Monday or Friday
        result *= random.uniform(0.9, 1.0)
    else:  # Tuesday to Thursday
        result *= random.uniform(1.0, 1.1)

    # Monthly pattern - often shows a spike at month end for batch processes
    day_of_month = current_date.day
    last_day_of_month = calendar.monthrange(
        current_date.year, current_date.month)[1]

    # Spike in usage near month end (last 3 days)
    if day_of_month >= last_day_of_month - 2:
        # 10-25% spike at month end
        result *= random.uniform(1.1, 1.25)

    return result


def pick_representative_projects():
    """
    Pick representative projects, ensuring diversity of lifecycle patterns.
    Selects at least one project for each lifecycle type and fills remaining slots.
    """
    projects = CONFIG["projects"]
    lifecycles = CONFIG["project_lifecycles"]

    # Determine desired number of projects (at most 7, but enough to cover all lifecycles)
    max_num_proj = DATA_VOLUME_SETTINGS["maximum_projects_to_be_picked"]
    max_projects = min(max_num_proj, len(projects))

    # Determine desired number of projects (at most 7, but enough to cover all lifecycles)
    # max_projects = min(7, len(projects))
    min_projects = min(len(lifecycles), max_projects)

    # Group projects by lifecycle
    lifecycle_projects = {lifecycle: [] for lifecycle in lifecycles}
    for proj_name, proj_data in projects.items():
        lifecycle = proj_data.get("lifecycle")
        if lifecycle in lifecycle_projects:
            lifecycle_projects[lifecycle].append(proj_name)

    # Ensure we have at least one project per lifecycle
    selected_projects = []

    # First ensure we have all lifecycle types represented if possible
    for lifecycle, proj_list in lifecycle_projects.items():
        if proj_list:
            # Select project with most diverse service mix for this lifecycle
            best_project = None
            max_service_diversity = -1

            for proj_name in proj_list:
                service_count = len(
                    set(projects[proj_name].get("services", [])))
                if service_count > max_service_diversity:
                    max_service_diversity = service_count
                    best_project = proj_name

            if best_project:
                selected_projects.append(best_project)

    # If we have too many projects (unlikely given the 6 lifecycle types), trim the list
    if len(selected_projects) > max_projects:
        selected_projects = selected_projects[:max_projects]

    # If we need more projects, add the most diverse remaining projects
    remaining_slots = max_projects - len(selected_projects)
    if remaining_slots > 0:
        candidate_projects = []
        for proj_name, proj_data in projects.items():
            if proj_name not in selected_projects:
                # Calculate a diversity score based on number of services, regions, etc.
                diversity_score = len(set(proj_data.get("services", []))) * 10
                diversity_score += len(set(proj_data.get("stages", []))) * 5

                candidate_projects.append((proj_name, diversity_score))

        # Sort by diversity score descending
        candidate_projects.sort(key=lambda x: x[1], reverse=True)

        # Add top N projects
        for i in range(min(remaining_slots, len(candidate_projects))):
            selected_projects.append(candidate_projects[i][0])

    return selected_projects


def find_missing_services():
    """
    Find services that are referenced in projects but not defined in AWS_SERVICES.
    Returns the missing services and adds default configurations for them.
    """
    referenced_services = set()
    for project_data in CONFIG["projects"].values():
        referenced_services.update(project_data.get("services", []))

    defined_services = set()
    for category_services in CONFIG["services"].values():
        defined_services.update(category_services.keys())

    missing = referenced_services - defined_services

    # Add default configurations for missing services
    if missing and "Management & Governance" in CONFIG["services"]:
        for service in missing:
            CONFIG["services"]["Management & Governance"][service] = {
                "base_rate": 0.05,
                "operations": ["ServiceOperations"],
                "price_range": (0.01, 0.1),
                "pricing_model": "on_demand",
                "unit": "Hrs",
                "usage_types": [f"{service}-Usage"]
            }

    return missing


def generate_resource_tags(resource_id, service_name, project_name, project_data, stage, instance_type=None):
    """
    Generate rich, realistic tags for AWS resources

    Args:
        resource_id: The AWS resource ID
        service_name: AWS service name
        project_name: Project name
        project_data: Project data dictionary
        stage: Deployment stage
        instance_type: Instance type (if applicable)

    Returns:
        List of tag dictionaries
    """
    tags = []

    # Common mandatory tags
    business_unit = project_data.get("business_unit", "")
    project_use_case = project_data.get("use_case", "")
    env_type = "Production" if "prod" in stage.lower() else "Non-Production"

    # Base tags that should be on every resource
    base_tags = [
        {"resourceId": resource_id, "key": "Name",
            "value": f"{project_name}-{service_name}"},
        {"resourceId": resource_id, "key": "Project", "value": project_name},
        {"resourceId": resource_id, "key": "BusinessUnit", "value": business_unit},
        {"resourceId": resource_id, "key": "Environment", "value": env_type},
        {"resourceId": resource_id, "key": "CostCenter",
            "value": f"{business_unit}-{random.randint(1000, 9999)}"},
    ]
    tags.extend(base_tags)

    # Add more dynamic base tags
    if project_use_case:
        tags.append({"resourceId": resource_id,
                    "key": "UseCase", "value": project_use_case})

    # Determine how many tags from each category to add for this resource
    # Different resources will have different tag coverage to reflect real-world variance
    technical_tags_count = random.randint(1, 3)
    business_tags_count = random.randint(1, 2)
    compliance_tags_count = random.randint(0, 2)
    automation_tags_count = random.randint(1, 2)
    finops_tags_count = random.randint(0, 2)

    # Boost compliance tags for production and sensitive resources
    if "prod" in stage.lower():
        compliance_tags_count += 1
        finops_tags_count += 1

    # Service-specific tag adjustments
    if service_name in ["RDS", "DynamoDB", "S3"]:
        compliance_tags_count += 1

    # Add tags from each category
    for category, count in [
        ("Technical", technical_tags_count),
        ("Business", business_tags_count),
        ("Compliance", compliance_tags_count),
        ("Automation", automation_tags_count),
        ("FinOps", finops_tags_count)
    ]:
        # Get available tags for this category
        available_tags = TAG_CATEGORIES.get(category, [])

        # Skip if no tags available
        if not available_tags:
            continue

        # Select random tags from this category
        selected_indices = random.sample(
            range(len(available_tags)), min(count, len(available_tags)))

        for idx in selected_indices:
            tag_spec = available_tags[idx]
            key = tag_spec["key"]

            # Skip if already added (from base tags)
            if key in [t["key"] for t in tags]:
                continue

            # Determine value
            if tag_spec["values"] is None:
                # Dynamic values
                if key == "Name":
                    value = f"{project_name}-{service_name}-{random.randint(1, 999)}"
                elif key == "CostCenter":
                    value = f"{business_unit}-{random.randint(1000, 9999)}"
                else:
                    value = "Unknown"
            else:
                # Randomly select from provided values
                value = random.choice(tag_spec["values"])

            tags.append({"resourceId": resource_id,
                        "key": key, "value": value})

    # Add service-specific tags
    if service_name in SERVICE_SPECIFIC_TAGS:
        service_tags = SERVICE_SPECIFIC_TAGS[service_name]

        # Determine how many service-specific tags to add (at least 1, at most all)
        service_tags_count = random.randint(1, len(service_tags))
        selected_indices = random.sample(
            range(len(service_tags)), service_tags_count)

        for idx in selected_indices:
            tag_spec = service_tags[idx]
            key = tag_spec["key"]

            # Skip if already added
            if key in [t["key"] for t in tags]:
                continue

            # Determine value
            if tag_spec["values"] is None:
                # Dynamic values
                if key == "InstanceType" and instance_type:
                    value = instance_type
                else:
                    value = "default"
            else:
                # Randomly select from provided values
                value = random.choice(tag_spec["values"])

            tags.append({"resourceId": resource_id,
                        "key": key, "value": value})

    # Add region consistency - consistent service tags across regions for the same service
    if random.random() < 0.8:  # 80% chance of having consistent service metadata
        tags.append({"resourceId": resource_id, "key": "ServiceTier",
                    "value": f"{service_name.lower()}-{random.choice(['standard', 'premium', 'basic', 'enterprise'])}"})

    # Random team tag
    if random.random() < 0.6:
        tags.append({"resourceId": resource_id, "key": "Team",
                    "value": random.choice([
                        "DevOps", "Platform", "Infrastructure", "Application",
                        "DataEngineering", "Analytics", "SRE", "Security"
                    ])})

    # Add chargeback tags
    chargeback_tags = generate_chargeback_tags(
        resource_id, service_name, project_name, project_data, stage)
    tags.extend(chargeback_tags)

    return tags


def generate_chargeback_tags(resource_id, service_name, project_name, project_data, stage_name):
    """Generate tags related to chargeback/showback models"""
    business_unit = project_data.get("business_unit", "")
    chargeback_tags = []

    # Determine if this is a shared resource or direct resource
    is_shared_resource = False
    shared_resource_id = None

    # Check if this service is in any shared allocation categories
    for allocation_rule, rule_data in COST_ALLOCATION_RULES.items():
        if service_name in rule_data["services"]:
            is_shared_resource = True
            shared_resource_id = allocation_rule
            break

    # Alternatively, check if this specific resource is in shared allocations
    if project_name in SHARED_RESOURCE_ALLOCATIONS:
        is_shared_resource = True
        shared_resource_id = project_name

    # Add basic chargeback tags
    chargeback_tags.append({"resourceId": resource_id, "key": "CostAllocation",
                           "value": "Direct" if not is_shared_resource else "Shared"})

    # Add more specific chargeback information for shared resources
    if is_shared_resource:
        allocation_model = "Unknown"
        for rule_name, rule_data in COST_ALLOCATION_RULES.items():
            if service_name in rule_data["services"]:
                allocation_model = rule_data["model"]
                break

        chargeback_tags.append({"resourceId": resource_id, "key": "AllocationMethod",
                               "value": allocation_model})

        if shared_resource_id in SHARED_RESOURCE_ALLOCATIONS:
            # Encode the actual allocation percentages
            allocation_json = json.dumps(
                SHARED_RESOURCE_ALLOCATIONS[shared_resource_id])
            chargeback_tags.append({"resourceId": resource_id, "key": "AllocationPercentages",
                                   "value": allocation_json})

    # Add department-specific tags
    department = None
    for tag in chargeback_tags:
        if tag["key"] == "Department":
            department = tag["value"]
            break

    if department:
        chargeback_tags.append({"resourceId": resource_id, "key": "ChargebackEntity",
                               "value": department})
    else:
        chargeback_tags.append({"resourceId": resource_id, "key": "ChargebackEntity",
                               "value": business_unit})

    # Add showback-specific flags
    if "prod" in stage_name.lower():
        chargeback_tags.append({"resourceId": resource_id, "key": "ShowbackCategory",
                               "value": "Production"})
    else:
        chargeback_tags.append({"resourceId": resource_id, "key": "ShowbackCategory",
                               "value": "Non-Production"})

    return chargeback_tags


def calculate_blended_unblended_rates(service_name, account_id, rate):
    """
    Calculate blended and unblended rates for a given service and account,
    taking into account Reserved Instance discounts
    """
    # Default: unblended = blended
    unblended_rate = rate
    blended_rate = rate

    # Apply service-specific RI discount factors if applicable
    if service_name in RI_DISCOUNT_MAPPING:
        service_discounts = RI_DISCOUNT_MAPPING[service_name]

        if account_id in service_discounts:
            # Unblended rate is the direct rate with account-specific discounts
            discount_factor = service_discounts[account_id]
            unblended_rate = rate * discount_factor

            # Blended rate is the organization-wide average
            # It tends to smooth out the discounts across accounts
            # For accounts with discounts, blended is higher than unblended
            # For accounts without discounts, blended is lower than unblended
            if discount_factor < 1.0:  # Account has a discount
                blended_factor = 1.0 - \
                    ((1.0 - discount_factor) * 0.5)  # Half the discount
                blended_rate = rate * blended_factor
            else:  # Account pays a premium
                # Most of premium removed
                blended_factor = 1.0 - ((discount_factor - 1.0) * 0.7)
                blended_rate = rate * blended_factor

    return unblended_rate, blended_rate


def generate_usage_data(project_name, project_data, day_count, start_date, daily_budget):
    """
    Generate usage data for a specific project.
    """
    results = []
    tags_data = []

    project_lifecycle = project_data.get("lifecycle", "steady_state")
    project_services = project_data.get("services", [])

    # Limit to a subset of services to reduce data volume
    max_services = DATA_VOLUME_SETTINGS["max_services_per_project"]
    if len(project_services) > max_services:
        project_services = random.sample(project_services, max_services)

    project_stages = project_data.get("stages", [])
    project_business_unit = project_data.get("business_unit", "")
    project_use_case = project_data.get("use_case", "")

    # Skip if no services or stages defined
    if not project_services or not project_stages:
        return results, tags_data

    # Assign regions based on data volume settings
    regions = CONFIG["AWS_REGIONS"]
    if not regions:
        regions = ["us-east-1", "us-west-2"]  # Default if no regions defined

    # Primary regions
    num_primary = min(
        DATA_VOLUME_SETTINGS["primary_regions_per_project"], len(regions))
    primary_regions = random.sample(regions, num_primary)

    # DR regions
    remaining_regions = [r for r in regions if r not in primary_regions]
    dr_regions = []
    if remaining_regions and random.random() < DATA_VOLUME_SETTINGS["dr_region_probability"]:
        dr_regions = [random.choice(remaining_regions)]

    # Determine service distribution (how much of daily budget goes to each service)
    service_weights = {}
    for svc in project_services:
        # Look up the service in the services config
        svc_found = False
        for category, services in CONFIG["services"].items():
            if svc in services:
                svc_found = True
                # Base weight on service price range
                price_range = services[svc].get("price_range", (0.01, 1.0))
                avg_price = (price_range[0] + price_range[1]) / 2
                service_weights[svc] = avg_price
                break

        if not svc_found:
            # Use default weight if service not found
            service_weights[svc] = 1.0

    # Normalize weights
    total_weight = sum(service_weights.values())
    if total_weight > 0:
        for svc in service_weights:
            service_weights[svc] /= total_weight

    # Determine stage distribution
    stage_weights = {}
    for stage in project_stages:
        if "prod" in stage.lower():
            stage_weights[stage] = 0.6  # Production gets most of the budget
        elif "staging" in stage.lower() or "test" in stage.lower():
            stage_weights[stage] = 0.3  # Staging/test environments
        else:
            stage_weights[stage] = 0.1  # Development and others

    # Normalize stage weights
    total_stage_weight = sum(stage_weights.values())
    if total_stage_weight > 0:
        for stage in stage_weights:
            stage_weights[stage] /= total_stage_weight

    # Calculate daily project budget (roughly 1/7 of total since we chose 7 projects)
    project_daily_budget = daily_budget / 7

    # Keep track of resource IDs to reuse them for the same service
    resource_ids = defaultdict(dict)  # {service: {region: [ids]}}

    # Process days based on sampling interval
    sampling_interval = DATA_VOLUME_SETTINGS["sampling_interval"]
    for day_idx in range(0, day_count, sampling_interval):
        current_date = start_date + datetime.timedelta(days=day_idx)

        # Skip weekends for certain services to simulate workday patterns
        is_weekend = current_date.weekday() >= 5  # 5=Saturday, 6=Sunday
        weekend_reduction_factor = 0.3 if is_weekend else 1.0

        # Apply lifecycle pattern to determine daily budget for this day
        volatility_factor = DATA_VOLUME_SETTINGS["volatility_factor"]
        lifecycle_factor = apply_lifecycle_pattern(
            day_idx, day_count, project_lifecycle, 1.0, volatility=volatility_factor)
        day_project_budget = project_daily_budget * \
            lifecycle_factor * weekend_reduction_factor

        # Generate data for each service and stage
        for service_name, service_weight in service_weights.items():
            service_budget = day_project_budget * service_weight

            for stage_name, stage_weight in stage_weights.items():
                stage_budget = service_budget * stage_weight
                account_id = get_account_id_for_stage(stage_name)

                # Determine if this service uses primary or DR region (or both)
                use_dr = random.random() < 0.2  # 20% chance of using DR region
                regions_to_use = primary_regions + \
                    (dr_regions if use_dr else [])

                # Distribute budget across regions
                region_weights = {}
                for region in regions_to_use:
                    # Apply regional cost factor
                    cost_factor = CONFIG["REGIONAL_COST_FACTORS"].get(
                        region, 1.0)
                    region_weights[region] = cost_factor

                # Normalize region weights
                total_region_weight = sum(region_weights.values())
                for region in region_weights:
                    region_weights[region] /= total_region_weight

                # Generate usage data for each region
                for region, region_weight in region_weights.items():
                    region_budget = stage_budget * region_weight

                    # Find service details
                    service_details = None
                    for category, services in CONFIG["services"].items():
                        if service_name in services:
                            service_details = services[service_name]
                            break

                    if not service_details:
                        continue

                    # Create or reuse resource IDs
                    if service_name not in resource_ids or region not in resource_ids[service_name]:
                        resource_ids[service_name][region] = []

                        # Generate resources based on settings
                        num_resources = DATA_VOLUME_SETTINGS["max_resources_per_service"]
                        for _ in range(num_resources):
                            instance_type = None
                            if "instance_types" in service_details and service_details["instance_types"]:
                                instance_type = random.choice(
                                    service_details["instance_types"])

                            resource_id = generate_resource_id(
                                service_name, region, instance_type)
                            resource_ids[service_name][region].append(
                                resource_id)

                            # Generate enhanced tags for this resource
                            tags = generate_resource_tags(
                                resource_id,
                                service_name,
                                project_name,
                                project_data,
                                stage_name,
                                instance_type
                            )
                            tags_data.extend(tags)

                    # Distribute budget across resources
                    num_resources = len(resource_ids[service_name][region])
                    resource_budget = region_budget / num_resources if num_resources > 0 else 0

                    for resource_id in resource_ids[service_name][region]:
                        if resource_budget <= 0:
                            continue

                        # Generate usage records based on settings
                        num_usage_records = random.randint(
                            1, DATA_VOLUME_SETTINGS["max_usage_records_per_day"])
                        for _ in range(num_usage_records):
                            line_item_type = random.choices(
                                LINE_ITEM_TYPES, weights=LINE_ITEM_TYPE_WEIGHTS)[0]

                            # Determine usage amount, rate, and cost
                            base_rate = service_details.get("base_rate", 0.01)

                            # Apply some randomness to the rate
                            rate_variability = random.uniform(0.9, 1.1)
                            rate = base_rate * rate_variability

                            unit = service_details.get("unit", "Hrs")

                            # Calculate unblended/blended rates
                            unblended_rate, blended_rate = calculate_blended_unblended_rates(
                                service_name, account_id, rate)

                            if line_item_type == "Usage":
                                # Calculate usage amount from budget and rate
                                usage_amount = resource_budget / unblended_rate / \
                                    num_usage_records if unblended_rate > 0 else 0
                                unblended_cost = usage_amount * unblended_rate
                                blended_cost = usage_amount * blended_rate
                            elif line_item_type == "Tax":
                                # Tax is typically a percentage of the cost
                                usage_amount = 1.0
                                tax_rate = resource_budget * 0.1 / num_usage_records  # 10% tax
                                unblended_cost = tax_rate
                                blended_cost = tax_rate  # Tax is the same for blended/unblended
                                unblended_rate = tax_rate
                                blended_rate = tax_rate
                            else:
                                # Other types have their own logic
                                usage_amount = resource_budget / unblended_rate / \
                                    num_usage_records / 2 if unblended_rate > 0 else 0
                                unblended_cost = usage_amount * unblended_rate
                                blended_cost = usage_amount * blended_rate

                            # Determine time interval for this usage
                            # Max 23 hours to ensure valid range
                            usage_hours = random.randint(1, 23)
                            usage_start = datetime.datetime.combine(
                                current_date,
                                datetime.time(
                                    hour=random.randint(0, 23-usage_hours))
                            )
                            usage_end = usage_start + \
                                datetime.timedelta(hours=usage_hours)

                            # Format according to AWS CUR format
                            time_interval = f"{usage_start.strftime('%Y-%m-%dT%H:%M:%S')}/{usage_end.strftime('%Y-%m-%dT%H:%M:%S')}"

                            # Billing period is typically monthly
                            billing_period_start = datetime.datetime(
                                current_date.year, current_date.month, 1
                            )

                            # Last day of the month
                            last_day = calendar.monthrange(
                                current_date.year, current_date.month)[1]
                            billing_period_end = datetime.datetime(
                                current_date.year, current_date.month, last_day, 23, 59, 59
                            )

                            # Generate invoice ID
                            first_day_of_month = current_date.replace(day=1)
                            invoice_id = f"{INVOICE_PREFIX}{first_day_of_month.strftime('%Y%m%d')}"

                            # Choose a random operation from service details
                            operations = service_details.get(
                                "operations", ["RunInstance"])
                            operation = operations[0] if operations else "RunInstance"
                            if len(operations) > 1:
                                operation = random.choice(operations)

                            # Choose a random usage type from service details
                            usage_types = service_details.get(
                                "usage_types", [f"{region}-{service_name}-Usage"])
                            usage_type = usage_types[0] if usage_types else f"{region}-{service_name}-Usage"
                            if len(usage_types) > 1:
                                usage_type = random.choice(usage_types)

                            # Generate availability zone
                            az = f"{region}{random.choice(['a', 'b', 'c'])}"

                            # Generate line item description
                            line_item_description = f"{service_name} {operation} in {region}"

                            # Create the record
                            record = {
                                "identity/LineItemId": str(uuid.uuid4()),
                                "identity/TimeInterval": time_interval,
                                "bill/InvoiceId": invoice_id,
                                "bill/BillingEntity": "AWS",
                                "bill/BillType": "Anniversary",
                                "bill/PayerAccountId": CONFIG["account_hierarchy"]["Organization"]["account_id"],
                                "bill/BillingPeriodStartDate": billing_period_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "bill/BillingPeriodEndDate": billing_period_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "lineItem/UsageAccountId": account_id,
                                "lineItem/LineItemType": line_item_type,
                                "lineItem/UsageStartDate": usage_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "lineItem/UsageEndDate": usage_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "lineItem/ProductCode": service_name,
                                "lineItem/UsageType": usage_type,
                                "lineItem/Operation": operation,
                                "lineItem/AvailabilityZone": az,
                                "lineItem/ResourceId": resource_id,
                                "lineItem/UsageAmount": usage_amount,
                                "lineItem/NormalizationFactor": "1",
                                "lineItem/NormalizedUsageAmount": usage_amount,
                                "lineItem/CurrencyCode": CURRENCY_CODE,
                                "lineItem/UnblendedRate": unblended_rate,
                                "lineItem/UnblendedCost": unblended_cost,
                                "lineItem/BlendedRate": blended_rate,
                                "lineItem/BlendedCost": blended_cost,
                                "lineItem/LineItemDescription": line_item_description,
                                "lineItem/TaxType": "Tax" if line_item_type == "Tax" else "",
                                "product/ProductName": service_name,
                                "product/servicecode": service_name.lower(),
                                "product/region": region,
                                "pricing/unit": unit,
                                "pricing/publicOnDemandCost": unblended_cost,  # Use unblended as public cost
                                "pricing/publicOnDemandRate": unblended_rate,
                                "pricing/term": "OnDemand",
                                "pricing/offeringClass": "Standard"
                            }

                            results.append(record)

                            # Subtract from budget for subsequent calculations
                            resource_budget -= unblended_cost

    return results, tags_data


def process_project(args):
    """Process a single project - for parallel execution"""
    project_name, project_data, day_count, start_date, daily_budget = args
    try:
        start_time = time.time()

        # Validate project data
        if not project_data.get("services"):
            print(
                f"Warning: Project {project_name} has no services defined. Skipping.")
            return [], []

        if not project_data.get("stages"):
            print(
                f"Warning: Project {project_name} has no stages defined. Skipping.")
            return [], []

        # Ensure lifecycle is valid
        if project_data.get("lifecycle") not in CONFIG["project_lifecycles"]:
            print(
                f"Warning: Project {project_name} has invalid lifecycle. Using 'steady_state'.")
            project_data["lifecycle"] = "steady_state"

        results, tags = generate_usage_data(
            project_name, project_data, day_count, start_date, daily_budget)
        end_time = time.time()
        print(
            f"Generated {len(results)} records for project {project_name} in {end_time - start_time:.2f} seconds")
        return results, tags
    except Exception as e:
        import traceback
        print(f"Error processing project {project_name}: {e}")
        print(traceback.format_exc())
        return [], []


def generate_project_lifecycle_mapping(selected_projects):
    """
    Generate a mapping of projects to their lifecycles

    Args:
        selected_projects: List of selected project names

    Returns:
        DataFrame with project details
    """
    project_details = []

    for project_name in selected_projects:
        project_data = CONFIG["projects"].get(project_name, {})

        # Collect project metadata
        lifecycle = project_data.get("lifecycle", "unknown")
        business_unit = project_data.get("business_unit", "")
        use_case = project_data.get("use_case", "")
        description = project_data.get("description", "")
        stages = ", ".join(project_data.get("stages", []))
        services = ", ".join(project_data.get("services", []))

        project_details.append({
            "project_name": project_name,
            "lifecycle": lifecycle,
            "business_unit": business_unit,
            "use_case": use_case,
            "description": description,
            "stages": stages,
            "services": services
        })

    return pd.DataFrame(project_details)


def generate_chargeback_reports(df_records, df_tags, output_dir):
    """Generate chargeback and showback reports based on cost data and tags"""

    # Create mapping from resource IDs to their chargeback entities
    resource_to_entity = {}
    resource_allocation_method = {}

    for _, tag in df_tags.iterrows():
        if tag['key'] == 'ChargebackEntity':
            resource_to_entity[tag['resourceId']] = tag['value']
        if tag['key'] == 'AllocationMethod':
            resource_allocation_method[tag['resourceId']] = tag['value']

    # Apply the mapping to get chargeback entity for each record
    df_records['chargeback_entity'] = df_records['lineItem/ResourceId'].map(
        resource_to_entity).fillna("Unallocated")

    df_records['allocation_method'] = df_records['lineItem/ResourceId'].map(
        resource_allocation_method).fillna("direct")

    # 1. Direct Chargeback Report - what each entity should be charged
    chargeback_summary = df_records.groupby(['month', 'chargeback_entity'])[
        'lineItem/UnblendedCost'].sum().reset_index()
    chargeback_summary.to_csv(
        f"{output_dir}/chargeback_by_entity.csv", index=False)

    # 2. Generate by Service and Entity
    service_entity_summary = df_records.groupby(
        ['month', 'chargeback_entity', 'lineItem/ProductCode'])['lineItem/UnblendedCost'].sum().reset_index()
    service_entity_summary.to_csv(
        f"{output_dir}/chargeback_by_service_entity.csv", index=False)

    # 3. Compare Blended vs Unblended for proper showback
    showback_comparison = df_records.groupby(['month', 'chargeback_entity'])[
        ['lineItem/UnblendedCost', 'lineItem/BlendedCost']].sum().reset_index()
    showback_comparison['cost_difference'] = showback_comparison['lineItem/BlendedCost'] - \
        showback_comparison['lineItem/UnblendedCost']
    showback_comparison['difference_percent'] = (showback_comparison['cost_difference'] /
                                                 showback_comparison['lineItem/UnblendedCost']) * 100
    showback_comparison.to_csv(
        f"{output_dir}/showback_blended_comparison.csv", index=False)

    # 4. Allocation Methods Report
    allocation_summary = df_records.groupby(['month', 'allocation_method'])[
        'lineItem/UnblendedCost'].sum().reset_index()
    allocation_summary.to_csv(
        f"{output_dir}/cost_by_allocation_method.csv", index=False)

    return {
        'chargeback_total': chargeback_summary['lineItem/UnblendedCost'].sum(),
        'direct_allocation': allocation_summary[allocation_summary['allocation_method'] == 'direct']['lineItem/UnblendedCost'].sum(),
        'shared_allocation': allocation_summary[allocation_summary['allocation_method'] != 'direct']['lineItem/UnblendedCost'].sum(),
    }


def analyze_blended_unblended_impact(df_records, output_dir):
    """Analyze the impact of blended vs unblended costs"""

    # Calculate the difference between blended and unblended costs
    df_records['cost_difference'] = df_records['lineItem/BlendedCost'] - \
        df_records['lineItem/UnblendedCost']
    df_records['is_discounted'] = df_records['cost_difference'] < 0

    # Summary by account
    account_summary = df_records.groupby(['lineItem/UsageAccountId'])[
        ['lineItem/UnblendedCost', 'lineItem/BlendedCost', 'cost_difference']].sum().reset_index()
    account_summary['discount_percent'] = (account_summary['cost_difference'] /
                                           account_summary['lineItem/UnblendedCost']) * 100
    account_summary.to_csv(
        f"{output_dir}/blended_unblended_by_account.csv", index=False)

    # Summary by service
    service_summary = df_records.groupby(['lineItem/ProductCode'])[
        ['lineItem/UnblendedCost', 'lineItem/BlendedCost', 'cost_difference']].sum().reset_index()
    service_summary['discount_percent'] = (service_summary['cost_difference'] /
                                           service_summary['lineItem/UnblendedCost']) * 100
    service_summary.to_csv(
        f"{output_dir}/blended_unblended_by_service.csv", index=False)

    # Find resources with the largest differences
    resource_summary = df_records.groupby(['lineItem/ResourceId'])[
        ['lineItem/UnblendedCost', 'lineItem/BlendedCost', 'cost_difference']].sum().reset_index()
    resource_summary = resource_summary.sort_values(
        'cost_difference', ascending=False)
    top_resources = resource_summary.head(20)
    top_resources.to_csv(
        f"{output_dir}/top_blended_unblended_impact_resources.csv", index=False)

    # Overall statistics
    total_unblended = df_records['lineItem/UnblendedCost'].sum()
    total_blended = df_records['lineItem/BlendedCost'].sum()
    total_difference = total_blended - total_unblended
    percent_difference = (total_difference / total_unblended) * \
        100 if total_unblended > 0 else 0

    summary_stats = {
        'total_unblended_cost': total_unblended,
        'total_blended_cost': total_blended,
        'total_difference': total_difference,
        'percent_difference': percent_difference,
        'accounts_with_savings': len(account_summary[account_summary['cost_difference'] < 0]),
        'accounts_paying_more': len(account_summary[account_summary['cost_difference'] > 0]),
    }

    # Save summary stats
    with open(f"{output_dir}/blended_unblended_summary.json", 'w') as f:
        json.dump(summary_stats, f, indent=2)

    return summary_stats


def main():
    print("AWS Cost and Usage Report Generator")
    print("Data Volume Settings:")
    for key, value in DATA_VOLUME_SETTINGS.items():
        print(f"  {key}: {value}")

    start_time = time.time()

    # Calculate daily budget
    daily_budget = calculate_daily_budget()
    print(f"Daily budget: ${daily_budget:.2f}")

    # Calculate number of days - REDUCED based on settings
    data_days = min(
        DATA_VOLUME_SETTINGS["days_to_generate"], CONFIG["number_of_days"])
    start_date = END_DATE - datetime.timedelta(days=data_days)
    day_count = (END_DATE - start_date).days
    print(
        f"Generating data for {day_count} days from {start_date} to {END_DATE}")
    print(f"Sampling every {DATA_VOLUME_SETTINGS['sampling_interval']} days")
    print(
        f"Using volatility factor of {DATA_VOLUME_SETTINGS['volatility_factor']} (±{DATA_VOLUME_SETTINGS['volatility_factor']*100}%)")

    # Pick representative projects with diverse lifecycles
    selected_projects = pick_representative_projects()
    print(f"Selected projects: {', '.join(selected_projects)}")

    # Generate project-lifecycle mapping
    project_lifecycle_df = generate_project_lifecycle_mapping(
        selected_projects)
    print("Generated project lifecycle mapping")

    # Check for missing services
    missing_services = find_missing_services()
    if missing_services:
        print(
            f"WARNING: Found services in projects that are not defined in AWS_SERVICES: {', '.join(missing_services)}")

    # Prepare arguments for parallel processing
    project_args = []
    for proj_name in selected_projects:
        proj_data = CONFIG["projects"].get(proj_name, {})
        project_args.append(
            (proj_name, proj_data, day_count, start_date, daily_budget))

    # Use multiprocessing to generate data in parallel
    all_records = []
    all_tags = []

    with multiprocessing.Pool(processes=min(len(project_args), multiprocessing.cpu_count())) as pool:
        results = pool.map(process_project, project_args)

        for records, tags in results:
            all_records.extend(records)
            all_tags.extend(tags)

    print(
        f"Generated {len(all_records)} total records and {len(all_tags)} tags")

    # Convert to DataFrames
    df_records = pd.DataFrame(all_records)
    df_tags = pd.DataFrame(all_tags)

    # Ensure all columns exist in the DataFrame
    for col in CUR_COLUMNS:
        if col not in df_records.columns:
            df_records[col] = ""

    for col in RESOURCE_TAGS_COLUMNS:
        if col not in df_tags.columns:
            df_tags[col] = ""

    # Save to CSV
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    df_records.to_csv(f"{output_dir}/cost_and_usage_report.csv", index=False)
    df_tags.to_csv(f"{output_dir}/resource_tags.csv", index=False)

    # Save the project lifecycle mapping
    project_lifecycle_df.to_csv(
        f"{output_dir}/project_lifecycle_mapping.csv", index=False)
    print(
        f"Saved project lifecycle mapping to {output_dir}/project_lifecycle_mapping.csv")

    # Generate a summary per project per month
    if not df_records.empty:
        # Convert timestamps to datetime
        df_records['month'] = pd.to_datetime(
            df_records['lineItem/UsageStartDate']).dt.strftime('%Y-%m')

        # Create a mapping of resource ID to project using tags
        resource_to_project = {}
        for _, tag in df_tags.iterrows():
            if tag['key'] == 'Project':
                resource_to_project[tag['resourceId']] = tag['value']

        # Apply mapping to get project for each record
        df_records['project'] = df_records['lineItem/ResourceId'].map(
            resource_to_project).fillna("Unknown")

        # Generate monthly cost summary by project
        summary = df_records.groupby(['month', 'project'])[
            'lineItem/UnblendedCost'].sum().reset_index()
        summary.to_csv(
            f"{output_dir}/cost_summary_by_project.csv", index=False)

        # Also generate summary by service
        service_summary = df_records.groupby(
            ['month', 'lineItem/ProductCode'])['lineItem/UnblendedCost'].sum().reset_index()
        service_summary.to_csv(
            f"{output_dir}/cost_summary_by_service.csv", index=False)

        # Generate summary by business unit
        # Create a mapping of project to business unit
        project_to_bu = {}
        for project_name in selected_projects:
            project_data = CONFIG["projects"].get(project_name, {})
            project_to_bu[project_name] = project_data.get(
                "business_unit", "Unknown")

        # Apply mapping to get business unit for each record
        df_records['business_unit'] = df_records['project'].map(
            project_to_bu).fillna("Unknown")

        # Generate monthly cost summary by business unit
        bu_summary = df_records.groupby(['month', 'business_unit'])[
            'lineItem/UnblendedCost'].sum().reset_index()
        bu_summary.to_csv(
            f"{output_dir}/cost_summary_by_business_unit.csv", index=False)

        # Generate chargeback/showback reports
        chargeback_stats = generate_chargeback_reports(
            df_records, df_tags, output_dir)
        print(
            f"Generated chargeback/showback reports. Total chargeback: ${chargeback_stats['chargeback_total']:.2f}")

        # Analyze blended vs unblended costs
        blended_impact = analyze_blended_unblended_impact(
            df_records, output_dir)
        print(f"Analyzed blended vs unblended costs. Difference: ${blended_impact['total_difference']:.2f} " +
              f"({blended_impact['percent_difference']:.2f}%)")

    end_time = time.time()
    print(f"Generated AWS CUR data in {end_time - start_time:.2f} seconds")
    print(f"Data saved to {output_dir}/")


if __name__ == "__main__":
    main()
