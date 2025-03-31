import pandas as pd
import numpy as np
from configGCP import CONFIG
from tqdm import tqdm
import time
import hashlib
import calendar
from collections import defaultdict
import json
import os
import multiprocessing
import datetime
import uuid
import random


def generate_tiered_rates(service_name, unit, effective_price):
    """Generate realistic tiered rates for services with tiered pricing"""

    # Services commonly using tiered pricing
    tiered_services = {
        "CloudStorage": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1024,
                    "unit_price": effective_price * 1.0},  # First 1TB
                {"start_usage_amount": 1024, "end_usage_amount": 10240,
                    "unit_price": effective_price * 0.9},  # Next 9TB
                {"start_usage_amount": 10240, "end_usage_amount": 51200,
                    "unit_price": effective_price * 0.8},  # Next 40TB
                {"start_usage_amount": 51200, "end_usage_amount": None,
                    "unit_price": effective_price * 0.7}   # Over 50TB
            ]
        },
        "BigQuery": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1,
                    "unit_price": effective_price * 1.0},      # First 1TB
                {"start_usage_amount": 1, "end_usage_amount": 10,
                    "unit_price": effective_price * 0.85},    # Next 9TB
                {"start_usage_amount": 10, "end_usage_amount": None,
                    "unit_price": effective_price * 0.65}  # Over 10TB
            ]
        },
        "CloudLogging": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 50,
                    "unit_price": 0.0},               # First 50GB free
                {"start_usage_amount": 50, "end_usage_amount": 100,
                    "unit_price": effective_price * 0.9},  # Next 50GB
                {"start_usage_amount": 100, "end_usage_amount": None,
                    "unit_price": effective_price}       # Over 100GB
            ]
        },
        "ComputeEngine": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.7}  # Sustained use discount
            ]
        },
        "CloudFunctions": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 2000000,
                    "unit_price": 0.0},                 # First 2M invocations free
                {"start_usage_amount": 2000000, "end_usage_amount": None,
                    "unit_price": effective_price}   # Over 2M invocations
            ]
        },
        "CloudRun": {
            "tiers": [
                # First 180K vCPU-seconds free
                {"start_usage_amount": 0, "end_usage_amount": 180000, "unit_price": 0.0},
                {"start_usage_amount": 180000, "end_usage_amount": None,
                    "unit_price": effective_price}    # Over 180K vCPU-seconds
            ]
        },
        "Pub/Sub": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 10,
                    "unit_price": 0.0},                      # First 10GB free
                {"start_usage_amount": 10, "end_usage_amount": 1024,
                    "unit_price": effective_price},       # Up to 1TB
                {"start_usage_amount": 1024, "end_usage_amount": 10240,
                    "unit_price": effective_price * 0.8},  # 1TB-10TB
                {"start_usage_amount": 10240, "end_usage_amount": None,
                    "unit_price": effective_price * 0.6}   # Over 10TB
            ]
        },
        "Dataflow": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 120,
                    "unit_price": effective_price},          # First 120 hours
                {"start_usage_amount": 120, "end_usage_amount": 730,
                    "unit_price": effective_price * 0.95},  # 120-730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.9}  # Over 730 hours
            ]
        },
        "Firestore": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1,
                    "unit_price": 0.0},                        # First 1GB stored
                {"start_usage_amount": 1, "end_usage_amount": 10,
                    "unit_price": effective_price},           # 1-10GB
                {"start_usage_amount": 10, "end_usage_amount": 100,
                    "unit_price": effective_price * 0.9},   # 10-100GB
                {"start_usage_amount": 100, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Over 100GB
            ]
        },
        "CloudMonitoring": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 150,
                    "unit_price": 0.0},                      # First 150MB free
                {"start_usage_amount": 150, "end_usage_amount": 100000,
                    "unit_price": effective_price},     # 150MB-100GB
                {"start_usage_amount": 100000, "end_usage_amount": None,
                    "unit_price": effective_price * 0.6}  # Over 100GB
            ]
        },
        "VPC": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1,
                    "unit_price": 0.0},                         # First 1GB free
                {"start_usage_amount": 1, "end_usage_amount": 1024,
                    "unit_price": effective_price},         # 1GB-1TB
                {"start_usage_amount": 1024, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Over 1TB
            ]
        },
        "CloudSQL": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.7}  # Continued use discount
            ]
        },
        "GKE": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Continued use discount
            ]
        },
        "CloudCDN": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 10240,
                    "unit_price": effective_price},        # First 10TB
                {"start_usage_amount": 10240, "end_usage_amount": 51200,
                    "unit_price": effective_price * 0.85},  # Next 40TB
                {"start_usage_amount": 51200, "end_usage_amount": 153600,
                    "unit_price": effective_price * 0.75},  # Next 100TB
                {"start_usage_amount": 153600, "end_usage_amount": None,
                    "unit_price": effective_price * 0.65}   # Over 150TB
            ]
        },
    }

    # Get tier info for the service, or create a simple one-tier model if not found
    if service_name in tiered_services:
        tiers = tiered_services[service_name]["tiers"]
    else:
        # For services without defined tiers, create a simple one-tier model
        tiers = [{"start_usage_amount": 0, "end_usage_amount": None,
                  "unit_price": effective_price}]

    # Format tier information
    tiered_rates = []
    for tier in tiers:
        tier_info = {
            "start_usage_amount": str(tier["start_usage_amount"]),
            "end_usage_amount": str(tier["end_usage_amount"]) if tier["end_usage_amount"] is not None else None,
            "unit_price": tier["unit_price"],
            "unit": unit
        }
        tiered_rates.append(tier_info)

    return tiered_rates


# Import configuration
# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Constants and helper variables
START_DATE = datetime.date.today(
) - datetime.timedelta(days=CONFIG["number_of_days"])
END_DATE = datetime.date.today()
CURRENCY_CODE = "USD"
INVOICE_ID_PREFIX = "BI-"

# Cost types
COST_TYPES = ["regular", "tax", "adjustment", "rounding_error"]
COST_TYPE_WEIGHTS = [0.90, 0.07, 0.02, 0.01]  # Probability weights

# Data volume reduction settings - adjust these to control the amount of data generated
DATA_VOLUME_SETTINGS = {
    # Number of projects to generate data for
    "maximum_projects_to_be_picked": 1,
    "days_to_generate": 11,                  # Number of days to generate data for
    "sampling_interval": 3,                   # Generate data every X days
    "max_services_per_project": 8,            # Limit number of services per project
    "max_resources_per_service": 3,           # Number of resources per service
    # Max usage records per day per resource
    "max_usage_records_per_day": 3,
    "primary_regions_per_project": 1,         # Number of primary regions
    "dr_region_probability": 0.2,             # Probability of using DR region
    "volatility_factor": 0.02,                # +/- 2% cost volatility by default
}

# Tag categories for more realistic labeling (GCP uses labels instead of tags)
LABEL_CATEGORIES = {
    "Technical": [
        {"key": "name", "values": None},  # Will be set dynamically
        {"key": "environment", "values": [
            "production", "development", "testing", "staging", "qa", "uat", "dr"]},
        {"key": "version", "values": [
            "1-0", "2-0", "3-0", "latest", "stable", "beta"]},
        {"key": "auto-shutdown", "values": [
            "true", "false", "weekends", "nights"]},
        {"key": "backup-frequency", "values": [
            "daily", "hourly", "weekly", "monthly", "none"]},
        {"key": "data-classification", "values": [
            "public", "internal", "confidential", "restricted"]},
    ],
    "Business": [
        {"key": "project", "values": None},  # Will be set from project name
        # Will be set from project data
        {"key": "business-unit", "values": None},
        {"key": "cost-center", "values": None},  # Will be generated dynamically
        {"key": "department", "values": [
            "it", "engineering", "finance", "marketing", "sales", "research", "operations"]},
        {"key": "owner", "values": ["john.doe@example.com", "jane.smith@example.com", "team-devops@example.com",
                                    "sre-team@example.com", "cloud-admin@example.com"]},
        {"key": "requestor", "values": ["john.doe@example.com", "jane.smith@example.com", "team-devops@example.com",
                                        "product-team@example.com", "project-manager@example.com"]},
    ],
    "Compliance": [
        {"key": "compliance-hipaa", "values": ["required", "not-required"]},
        {"key": "compliance-pci", "values": ["in-scope", "out-of-scope"]},
        {"key": "compliance-sox", "values": ["in-scope", "out-of-scope"]},
        {"key": "compliance-gdpr", "values": ["in-scope", "out-of-scope"]},
        {"key": "security-level", "values": [
            "low", "medium", "high", "critical"]},
        {"key": "compliance-status", "values": [
            "compliant", "non-compliant", "exempted", "under-review"]},
    ],
    "Automation": [
        {"key": "created-by", "values": [
            "terraform", "deployment-manager", "ansible", "console", "gcloud", "api"]},
        {"key": "managed-by", "values": [
            "cloudops", "devops", "sre", "platform", "manual"]},
        {"key": "iac", "values": ["true", "false"]},
        {"key": "auto-scaling", "values": ["enabled", "disabled"]},
        {"key": "deployment-group", "values": [
            "blue", "green", "canary", "main", "experiment"]},
    ],
    "FinOps": [
        {"key": "allow-spot", "values": ["true", "false"]},
        {"key": "optimization-priority", "values": [
            "cost", "performance", "availability", "balanced"]},
        {"key": "budget-alert", "values": ["low", "medium", "high", "exempt"]},
        {"key": "scheduled-downtime", "values": [
            "weekends", "nights", "never", "custom"]},
        {"key": "rightsizing", "values": [
            "optimized", "pending-review", "oversized", "exempt"]},
    ]
}

# Service-specific labels
SERVICE_SPECIFIC_LABELS = {
    "ComputeEngine": [
        {"key": "machine-type", "values": None},  # Will be set dynamically
        {"key": "image", "values": [
            "debian-10", "ubuntu-2004-lts", "cos-stable", "rhel-8", "windows-2019"]},
        {"key": "auto-shutdown", "values": [
            "true", "false", "weekends", "nights"]},
        {"key": "patch-group", "values": [
            "group1", "group2", "critical", "standard", "dev"]},
    ],
    "CloudStorage": [
        {"key": "storage-class", "values": [
            "standard", "nearline", "coldline", "archive"]},
        {"key": "encryption", "values": [
            "google-managed", "customer-managed", "customer-supplied"]},
        {"key": "public-access", "values": [
            "blocked", "allowed-read-only", "controlled"]},
        {"key": "lifecycle-policy", "values": [
            "30-day-transition", "90-day-archive", "1-year-deletion", "compliance-7-years"]},
    ],
    "CloudSQL": [
        {"key": "engine", "values": [
            "mysql", "postgres", "sqlserver"]},
        {"key": "ha-configuration", "values": ["true", "false"]},
        {"key": "backup-retention", "values": ["7", "14", "30", "90"]},
        {"key": "db-name", "values": ["prod-db",
                                      "dev-db", "test-db", "analytics-db"]},
    ],
    "CloudFunctions": [
        {"key": "runtime", "values": [
            "python310", "nodejs16", "nodejs18", "go119", "java17", "php81", "ruby30"]},
        {"key": "memory-size", "values": ["128",
                                          "256", "512", "1024", "2048", "4096"]},
        {"key": "timeout", "values": ["30", "60", "300", "540"]},
        {"key": "event-trigger", "values": [
            "http", "cloud-storage", "pub-sub", "firestore", "scheduler"]},
    ],
    "Firestore": [
        {"key": "database-type", "values": [
            "native", "datastore"]},
        {"key": "mode", "values": ["native", "datastore"]},
        {"key": "location-type", "values": [
            "regional", "multi-regional", "dual-regional"]},
        {"key": "ttl", "values": ["enabled", "disabled"]},
    ],
    "PersistentDisk": [
        {"key": "disk-type", "values": [
            "pd-standard", "pd-balanced", "pd-ssd", "pd-extreme"]},
        {"key": "encrypted", "values": ["google-managed", "customer-managed"]},
        {"key": "snapshot-schedule", "values": [
            "daily", "weekly", "monthly", "none"]},
        {"key": "delete-with-instance", "values": ["true", "false"]},
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
        "allocation_key": "compute_usage",
        "entities": ["IT", "Finance", "Marketing", "Sales", "Operations", "Engineering"],
        "services": ["VPC", "CloudInterconnect", "CloudDNS", "CloudLogging", "SecurityCommandCenter"]
    },
    "data_services": {
        "model": "direct",
        "allocation_key": "data_volume",
        "entities": ["Analytics", "DataScience", "ProductDevelopment"],
        "services": ["CloudStorage", "CloudSQL", "Firestore", "BigQuery", "Dataflow"]
    },
    "security_compliance": {
        "model": "equal",
        "allocation_key": None,
        "entities": ["IT", "SecurityOperations", "Compliance", "Legal", "Finance"],
        "services": ["SecurityCommandCenter", "IAM", "KeyManagementService", "CloudArmor", "SecurityCommandCenter"]
    }
}

# Different allocation percentages for shared resources
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

# Committed use discount (CUD) benefit mapping for effective cost simulation
CUD_DISCOUNT_MAPPING = {
    "ComputeEngine": {
        # Mapping projects to discount factors
        # Values <1 indicate discount (project owns CUDs)
        # Values >1 indicate paying the premium (project uses shared resources)
        "shared-services-666666": 0.7,     # Shared services with 30% CUD discount
        "security-central-555555": 0.85,   # Security with 15% CUD discount
        "aviation-dev-222201": 1.05,       # Aviation Dev pays 5% more
        "aviation-prod-444401": 0.9,       # Aviation Prod gets 10% CUD discount
    },
    "CloudSQL": {
        "shared-services-666666": 0.75,    # Shared services with 25% CUD discount
        "pharma-prod-444402": 0.95,        # Pharma Prod with 5% CUD discount
    }
}

# GCP Billing BigQuery Export Schema columns
BIGQUERY_EXPORT_COLUMNS = [
    "billing_account_id",
    "service.id",
    "service.description",
    "sku.id",
    "sku.description",
    "usage_start_time",
    "usage_end_time",
    "project.id",
    "project.number",
    "project.name",
    "project.ancestry_numbers",
    "project.labels",
    "location.location",
    "location.country",
    "location.region",
    "location.zone",
    "export_time",
    "cost",
    "currency",
    "currency_conversion_rate",
    "usage.amount",
    "usage.unit",
    "usage.amount_in_pricing_units",
    "usage.pricing_unit",
    "credits",
    "invoice.month",
    "cost_type",
    "adjustment_info.id",
    "adjustment_info.description",
    "adjustment_info.mode",
    "system_labels",
    "resource.name",
    "resource.global_name",
    "price.effective_price",
    "price.tier",
    "price.tiered_rates"
]

# Resource Labels columns
RESOURCE_LABELS_COLUMNS = [
    "resource_name",
    "key",
    "value"
]


def calculate_daily_budget():
    """Calculate daily budget from annual budget"""
    annual_budget = CONFIG["annual_budget"]
    daily_budget = annual_budget / 365.0
    return daily_budget


def get_project_details(stage_name):
    """Find project ID, number, and name for a given stage name"""
    # Use direct mapping from config if available
    stage_map = CONFIG.get("STAGE_TO_PROJECT_MAPPING", {})

    # Normalize the stage name for matching
    stage_name_normalized = stage_name.lower().replace('_', '-')

    # First try direct match with the normalized stage name
    if stage_name_normalized in stage_map:
        return stage_map[stage_name_normalized]

    # Try exact match with original stage name
    if stage_name in stage_map:
        return stage_map[stage_name]

    # Try to find a partial match where stage_name contains or is contained in a key
    for key, value in stage_map.items():
        key_normalized = key.lower().replace('_', '-')
        if stage_name_normalized in key_normalized or key_normalized in stage_name_normalized:
            return value

    # If still no match, identify business unit from stage name
    business_unit = None
    for bu in ["aviation", "pharma", "manufacturing", "supplychain", "softwaresolutions", "ml"]:
        if bu in stage_name_normalized:
            business_unit = bu.capitalize()
            break

    if not business_unit:
        # Try to match to a business unit by looking at the stage name parts
        stage_parts = stage_name_normalized.split('-')
        for part in stage_parts:
            if part in ["dev", "staging", "prod", "test"]:
                # This is likely an environment part, not a business unit
                continue
            # Check if this part identifies a business unit
            for bu in ["aviation", "pharma", "manufacturing", "supply", "software", "ml"]:
                if bu in part or part in bu:
                    business_unit = bu.capitalize()
                    break

    # Default to Core if no business unit can be identified
    if not business_unit:
        business_unit = "Core"

    # Create a deterministic project ID based on the stage name
    # This ensures consistent IDs for the same stage names across runs
    stage_hash = hashlib.md5(stage_name_normalized.encode()).hexdigest()[:8]
    project_number = int(
        f"1{stage_hash}", 16) % 1000000000000  # 12-digit number

    # Format project name nicely
    name_parts = stage_name_normalized.split('-')
    formatted_parts = []
    for part in name_parts:
        if part in ["dev", "staging", "test", "prod"]:
            if part == "dev":
                formatted_parts.append("Development")
            elif part == "staging":
                formatted_parts.append("Staging")
            elif part == "test":
                formatted_parts.append("Test")
            elif part == "prod":
                formatted_parts.append("Production")
        else:
            formatted_parts.append(part.capitalize())

    project_name = f"{business_unit} {' '.join(formatted_parts)}"

    return {
        "project_id": f"{business_unit.lower()}-{stage_name_normalized}-{stage_hash[:4]}",
        "project_number": str(project_number),
        "project_name": project_name
    }


def get_billing_account_for_project(project_name):
    """Get the billing account ID for a project"""
    project_billing_mapping = CONFIG["project_billing_mapping"]
    billing_accounts = CONFIG["billing_accounts"]

    # Normalize project name for matching
    project_name_normalized = project_name.lower().replace('_', '-')

    # Try exact match first
    if project_name in project_billing_mapping:
        billing_key = project_billing_mapping[project_name]
        return billing_accounts[billing_key]["id"]

    # Try normalized match
    for mapping_name, billing_key in project_billing_mapping.items():
        mapping_normalized = mapping_name.lower().replace('_', '-')

        # Check if either name contains the other
        if mapping_normalized in project_name_normalized or project_name_normalized in mapping_normalized:
            return billing_accounts[billing_key]["id"]

    # Check for specific environments in the project name
    if "dev" in project_name_normalized or "sandbox" in project_name_normalized:
        return billing_accounts["development"]["id"]
    elif "research" in project_name_normalized:
        return billing_accounts["research"]["id"]

    # Default to primary billing account
    return billing_accounts["primary"]["id"]


def generate_resource_name(service_name, project_name, region=None, zone=None, machine_type=None):
    """Generate a realistic GCP resource name based on service type"""
    # Create a consistent hash based on project name and service
    name_base = f"{project_name}-{service_name}"
    hash_seed = int(hashlib.md5(name_base.encode()).hexdigest(), 16)
    random.seed(hash_seed)
    unique_id = ''.join(random.choices(
        'abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    random.seed()  # Reset the random seed

    # Create a shorter project identifier from the project name
    project_prefix = ''.join([word[0]
                             for word in project_name.split() if word]).lower()
    if len(project_prefix) < 2:
        project_prefix = project_name[:3].lower()

    # Generate names based on GCP naming conventions
    if service_name == "ComputeEngine":
        # Compute Engine instance naming convention
        purpose = random.choice(
            ['web', 'app', 'db', 'api', 'worker', 'batch', 'test'])
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        if machine_type:
            # First letter of size (e.g., 's' from 'standard')
            size = machine_type.split('-')[-1][0]
        else:
            size = random.choice(['s', 'm', 'l', 'xl'])

        return f"{project_prefix}-{purpose}-{env}-{size}-{unique_id[:4]}"

    elif service_name == "CloudStorage":
        # Cloud Storage bucket naming convention (globally unique, lowercase)
        purpose = random.choice(
            ['assets', 'data', 'backup', 'archive', 'media', 'logs'])
        return f"{project_prefix}-{purpose}-{unique_id}"

    elif service_name == "CloudSQL":
        # Cloud SQL instance naming convention
        db_type = random.choice(['mysql', 'postgres', 'sqlserver'])
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        return f"{project_prefix}-{db_type}-{env}-{unique_id[:4]}"

    elif service_name == "CloudFunctions":
        # Cloud Functions naming convention
        purpose = random.choice(
            ['process', 'transform', 'api', 'auth', 'notify', 'schedule', 'trigger'])
        return f"{project_prefix}-{purpose}-func-{unique_id[:4]}"

    elif service_name == "Firestore":
        # Firestore is typically referred to by collection/document, not resource name
        return f"{project_prefix}-firestore-{unique_id[:4]}"

    elif service_name == "PersistentDisk":
        # Persistent Disk naming convention
        disk_type = "ssd" if random.random() > 0.3 else "std"
        purpose = random.choice(['boot', 'data', 'temp', 'swap', 'cache'])
        return f"{project_prefix}-{disk_type}-{purpose}-{unique_id[:4]}"

    elif service_name == "CloudCDN":
        # CDN naming convention
        return f"{project_prefix}-cdn-{unique_id[:4]}"

    elif service_name == "BigQuery":
        # BigQuery dataset naming convention
        purpose = random.choice(
            ['analytics', 'reporting', 'warehouse', 'staging', 'metrics'])
        return f"{project_prefix}_{purpose}_{unique_id[:4]}"

    elif service_name == "GKE":
        # GKE cluster naming convention
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        return f"{project_prefix}-{env}-cluster-{unique_id[:4]}"

    elif service_name == "CloudRun":
        # Cloud Run service naming convention
        purpose = random.choice(
            ['api', 'web', 'worker', 'processor', 'service'])
        return f"{project_prefix}-{purpose}-{unique_id[:4]}"

    else:
        # Generic naming for other services
        service_short = ''.join(
            [word[0] for word in service_name.split() if word]).lower()
        if len(service_short) < 2:
            service_short = service_name[:3].lower()

        return f"{project_prefix}-{service_short}-{unique_id[:4]}"


def generate_system_labels(service_name, resource_name, project_id, region=None, zone=None, machine_type=None):
    """Generate system labels for GCP resources"""
    system_labels = {}

    # Create consistent resource IDs based on resource name
    resource_hash = hashlib.md5(resource_name.encode()).hexdigest()
    numeric_id = str(int(resource_hash[:16], 16))[:10]

    # Common system labels for all resources
    system_labels["compute.googleapis.com/resource_name"] = resource_name
    system_labels["goog-resource-family"] = service_name.lower().replace(" ", "-")

    # Add creation timestamp (slightly in the past)
    days_ago = random.randint(1, 180)
    creation_time = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    system_labels["goog-creation-time"] = creation_time.strftime(
        "%Y-%m-%dT%H:%M:%SZ")

    # Add location info
    if region:
        system_labels["cloud.googleapis.com/location"] = region
    if zone:
        system_labels["cloud.googleapis.com/zone"] = zone

    # Service-specific labels
    if service_name == "ComputeEngine":
        system_labels["compute.googleapis.com/resource_id"] = numeric_id
        if machine_type:
            system_labels["compute.googleapis.com/machine_type"] = machine_type
        if zone:
            system_labels["compute.googleapis.com/zone"] = zone
        # Add network info
        system_labels["compute.googleapis.com/network"] = f"projects/{project_id}/global/networks/default"
        system_labels["compute.googleapis.com/subnet"] = f"projects/{project_id}/regions/{region}/subnetworks/default"

    elif service_name == "CloudStorage":
        bucket_id = resource_hash
        system_labels["storage.googleapis.com/bucket_id"] = bucket_id
        system_labels["storage.googleapis.com/bucket_name"] = resource_name
        storage_class = random.choice(
            ["STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"])
        system_labels["storage.googleapis.com/storage_class"] = storage_class
        # Storage is typically regional or multi-regional
        if region:
            location_type = random.choice(["REGIONAL", "MULTI_REGIONAL"])
            system_labels["storage.googleapis.com/location_type"] = location_type
            system_labels["storage.googleapis.com/location"] = region if location_type == "REGIONAL" else random.choice([
                                                                                                                        "US", "EU", "ASIA"])

    elif service_name == "CloudSQL":
        system_labels["cloudsql.googleapis.com/instance_id"] = numeric_id
        system_labels["cloudsql.googleapis.com/database_name"] = resource_name
        db_version = random.choice(
            ["MYSQL_5_7", "MYSQL_8_0", "POSTGRES_13", "POSTGRES_14", "SQLSERVER_2019_STANDARD"])
        system_labels["cloudsql.googleapis.com/database_version"] = db_version
        system_labels["cloudsql.googleapis.com/tier"] = random.choice(
            ["db-n1-standard-1", "db-n1-standard-2", "db-n1-standard-4", "db-n1-standard-8"])
        if region:
            system_labels["cloudsql.googleapis.com/region"] = region

    elif service_name == "CloudFunctions":
        system_labels["cloudfunctions.googleapis.com/function_id"] = numeric_id
        system_labels["cloudfunctions.googleapis.com/function_name"] = resource_name
        system_labels["cloudfunctions.googleapis.com/runtime"] = random.choice(
            ["python310", "nodejs16", "go119", "java17"])
        trigger_type = random.choice(
            ["http", "pubsub", "storage", "firestore"])
        system_labels["cloudfunctions.googleapis.com/trigger_type"] = trigger_type

    elif service_name == "BigQuery":
        dataset_id = resource_name.split(
            '_')[1] if '_' in resource_name else resource_name
        table_id = f"table_{resource_hash[:8]}"
        system_labels["bigquery.googleapis.com/dataset_id"] = dataset_id
        system_labels["bigquery.googleapis.com/table_id"] = table_id

    elif service_name == "GKE":
        system_labels["container.googleapis.com/cluster_id"] = numeric_id
        system_labels["container.googleapis.com/cluster_name"] = resource_name
        system_labels["container.googleapis.com/cluster_location"] = region
        system_labels["container.googleapis.com/node_count"] = str(
            random.randint(3, 10))

    elif service_name == "CloudRun":
        system_labels["run.googleapis.com/service_id"] = numeric_id
        system_labels["run.googleapis.com/service_name"] = resource_name
        system_labels["run.googleapis.com/ingress"] = random.choice(
            ["all", "internal", "internal-and-cloud-load-balancing"])

    elif service_name == "Pub/Sub":
        system_labels["pubsub.googleapis.com/topic_id"] = f"{resource_name}-topic"
        system_labels["pubsub.googleapis.com/subscription_id"] = f"{resource_name}-sub"

    return system_labels


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

    # Determine desired number of projects
    max_num_proj = DATA_VOLUME_SETTINGS["maximum_projects_to_be_picked"]
    max_projects = min(max_num_proj, len(projects))

    # Determine minimum number of projects (at least one per lifecycle if possible)
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

    # If we have too many projects, trim the list
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
    Find services that are referenced in projects but not defined in GCP_SERVICES.
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
    if missing and "Management" in CONFIG["services"]:
        for service in missing:
            CONFIG["services"]["Management"][service] = {
                "base_rate": 0.05,
                "operations": ["ServiceOperations"],
                "price_range": (0.01, 0.1),
                "pricing_model": "on_demand",
                "unit": "hour",
                "usage_types": [f"{service}-Usage"],
                "sku_name_pattern": f"{service} {{operation}} in {{region}}",
                "sku_ids": [f"{uuid.uuid4().hex[:12].upper()}"]
            }

    return missing


def generate_resource_labels(resource_name, service_name, project_name, project_data, stage, machine_type=None):
    """
    Generate rich, realistic labels for GCP resources

    Args:
        resource_name: The GCP resource name
        service_name: GCP service name
        project_name: Project name
        project_data: Project data dictionary
        stage: Deployment stage
        machine_type: Machine type (if applicable)

    Returns:
        List of label dictionaries
    """
    labels = []

    # Common mandatory labels
    business_unit = project_data.get("business_unit", "")
    project_use_case = project_data.get("use_case", "")
    env_type = "production" if "prod" in stage.lower() else "non-production"

    # Base labels that should be on every resource
    base_labels = [
        {"resource_name": resource_name, "key": "name",
            "value": f"{project_name}-{service_name}"},
        {"resource_name": resource_name, "key": "project", "value": project_name},
        {"resource_name": resource_name,
            "key": "business-unit", "value": business_unit},
        {"resource_name": resource_name, "key": "environment", "value": env_type},
        {"resource_name": resource_name, "key": "cost-center",
            "value": f"{business_unit}-{random.randint(1000, 9999)}"},
    ]
    labels.extend(base_labels)

    # Add more dynamic base labels
    if project_use_case:
        labels.append({"resource_name": resource_name,
                       "key": "use-case", "value": project_use_case})

    # Determine how many labels from each category to add for this resource
    technical_labels_count = random.randint(1, 3)
    business_labels_count = random.randint(1, 2)
    compliance_labels_count = random.randint(0, 2)
    automation_labels_count = random.randint(1, 2)
    finops_labels_count = random.randint(0, 2)

    # Boost compliance labels for production and sensitive resources
    if "prod" in stage.lower():
        compliance_labels_count += 1
        finops_labels_count += 1

    # Service-specific label adjustments
    if service_name in ["CloudSQL", "Firestore", "CloudStorage"]:
        compliance_labels_count += 1

    # Add labels from each category
    for category, count in [
        ("Technical", technical_labels_count),
        ("Business", business_labels_count),
        ("Compliance", compliance_labels_count),
        ("Automation", automation_labels_count),
        ("FinOps", finops_labels_count)
    ]:
        # Get available labels for this category
        available_labels = LABEL_CATEGORIES.get(category, [])

        # Skip if no labels available
        if not available_labels:
            continue

        # Select random labels from this category
        selected_indices = random.sample(
            range(len(available_labels)), min(count, len(available_labels)))

        for idx in selected_indices:
            label_spec = available_labels[idx]
            key = label_spec["key"]

            # Skip if already added (from base labels)
            if key in [t["key"] for t in labels]:
                continue

            # Determine value
            if label_spec["values"] is None:
                # Dynamic values
                if key == "name":
                    value = f"{project_name}-{service_name}-{random.randint(1, 999)}"
                elif key == "cost-center":
                    value = f"{business_unit}-{random.randint(1000, 9999)}"
                else:
                    value = "unknown"
            else:
                # Randomly select from provided values
                value = random.choice(label_spec["values"])

            labels.append({"resource_name": resource_name,
                           "key": key, "value": value})

    # Add service-specific labels
    if service_name in SERVICE_SPECIFIC_LABELS:
        service_labels = SERVICE_SPECIFIC_LABELS[service_name]

        # Determine how many service-specific labels to add (at least 1, at most all)
        service_labels_count = random.randint(1, len(service_labels))
        selected_indices = random.sample(
            range(len(service_labels)), service_labels_count)

        for idx in selected_indices:
            label_spec = service_labels[idx]
            key = label_spec["key"]

            # Skip if already added
            if key in [t["key"] for t in labels]:
                continue

            # Determine value
            if label_spec["values"] is None:
                # Dynamic values
                if key == "machine-type" and machine_type:
                    value = machine_type
                else:
                    value = "default"
            else:
                # Randomly select from provided values
                value = random.choice(label_spec["values"])

            labels.append({"resource_name": resource_name,
                           "key": key, "value": value})

    # Add region consistency - consistent service labels across regions for the same service
    if random.random() < 0.8:  # 80% chance of having consistent service metadata
        labels.append({"resource_name": resource_name, "key": "service-tier",
                       "value": f"{service_name.lower()}-{random.choice(['standard', 'premium', 'basic', 'enterprise'])}"})

    # Random team label
    if random.random() < 0.6:
        labels.append({"resource_name": resource_name, "key": "team",
                       "value": random.choice([
                           "devops", "platform", "infrastructure", "application",
                           "data-engineering", "analytics", "sre", "security"
                       ])})

    # Add chargeback labels
    chargeback_labels = generate_chargeback_labels(
        resource_name, service_name, project_name, project_data, stage)
    labels.extend(chargeback_labels)

    return labels


def generate_chargeback_labels(resource_name, service_name, project_name, project_data, stage_name):
    """Generate labels related to chargeback/showback models"""
    business_unit = project_data.get("business_unit", "")
    chargeback_labels = []

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

    # Add basic chargeback labels
    chargeback_labels.append({"resource_name": resource_name, "key": "cost-allocation",
                              "value": "direct" if not is_shared_resource else "shared"})

    # Add more specific chargeback information for shared resources
    if is_shared_resource:
        allocation_model = "unknown"
        for rule_name, rule_data in COST_ALLOCATION_RULES.items():
            if service_name in rule_data["services"]:
                allocation_model = rule_data["model"]
                break

        chargeback_labels.append({"resource_name": resource_name, "key": "allocation-method",
                                  "value": allocation_model})

        if shared_resource_id in SHARED_RESOURCE_ALLOCATIONS:
            # Encode the actual allocation percentages - use simplified values
            # GCP labels don't allow complex values like JSON
            for entity, percentage in SHARED_RESOURCE_ALLOCATIONS[shared_resource_id].items():
                chargeback_labels.append({
                    "resource_name": resource_name,
                    "key": f"allocation-{entity.lower()}",
                    "value": str(int(percentage * 100))
                })

    # Add department-specific labels
    department = None
    for label in chargeback_labels:
        if label["key"] == "department":
            department = label["value"]
            break

    if department:
        chargeback_labels.append({"resource_name": resource_name, "key": "chargeback-entity",
                                  "value": department})
    else:
        chargeback_labels.append({"resource_name": resource_name, "key": "chargeback-entity",
                                  "value": business_unit})

    # Add showback-specific flags
    if "prod" in stage_name.lower():
        chargeback_labels.append({"resource_name": resource_name, "key": "showback-category",
                                  "value": "production"})
    else:
        chargeback_labels.append({"resource_name": resource_name, "key": "showback-category",
                                  "value": "non-production"})

    return chargeback_labels


def calculate_effective_price(service_name, project_id, base_price):
    """
    Calculate effective price for a given service and project,
    taking into account Committed Use Discounts (CUDs)
    """
    effective_price = base_price

    # Apply service-specific CUD discount factors if applicable
    if service_name in CUD_DISCOUNT_MAPPING:
        service_discounts = CUD_DISCOUNT_MAPPING[service_name]

        if project_id in service_discounts:
            # Apply the discount factor to the base price
            discount_factor = service_discounts[project_id]
            effective_price = base_price * discount_factor

    return effective_price


def generate_credits(service_name, cost, project_id):
    """Generate credit information if applicable"""
    credits = []

    # Only generate credits for certain conditions
    if cost > 10 and random.random() < 0.3:  # 30% chance for high-cost items
        credit_types = [
            {"name": "Committed Use Discount", "id": "cud-1yr",
                "full_name": "Committed Use Discount: 1 year"},
            {"name": "Sustained Use Discount", "id": "sustained-use-discount",
                "full_name": "Sustained Use Discount"},
            {"name": "Spend-based Discount", "id": "spend-based-discount",
                "full_name": "Spend-based Committed Use Discount"}
        ]

        # Pick one credit type
        credit_type = random.choice(credit_types)

        # Calculate credit amount (between 10% and 30% of the cost)
        credit_percent = random.uniform(0.1, 0.3)
        credit_amount = -1 * cost * credit_percent  # Credits are negative

        credit = {
            "name": credit_type["name"],
            "full_name": credit_type["full_name"],
            "type": credit_type["id"],
            "id": f"{credit_type['id']}-{uuid.uuid4().hex[:8]}",
            "amount": credit_amount
        }

        credits.append(credit)

    return credits


def generate_usage_data(project_name, project_data, day_count, start_date, daily_budget):
    """
    Generate usage data for a specific project following GCP billing format.
    """
    results = []
    labels_data = []

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
        return results, labels_data

    # Assign regions based on data volume settings
    regions = CONFIG["gcp_regions"]
    if not regions:
        regions = ["us-central1", "us-east1"]  # Default if no regions defined

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

    # Calculate daily project budget (roughly 1/N of total since we chose N projects)
    num_projects = DATA_VOLUME_SETTINGS["maximum_projects_to_be_picked"]
    project_daily_budget = daily_budget / num_projects

    # Keep track of resource names to reuse them for the same service
    resource_names = defaultdict(dict)  # {service: {region: [names]}}

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

                # Get project details
                project_details = get_project_details(stage_name)
                project_id = project_details["project_id"]
                project_number = project_details["project_number"]
                project_display_name = project_details["project_name"]

                # Get billing account for this project
                billing_account_id = get_billing_account_for_project(
                    project_display_name)

                # Determine if this service uses primary or DR region (or both)
                use_dr = random.random() < 0.2  # 20% chance of using DR region
                regions_to_use = primary_regions + \
                    (dr_regions if use_dr else [])

                # Distribute budget across regions
                region_weights = {}
                for region in regions_to_use:
                    # Apply regional cost factor
                    cost_factor = CONFIG["regional_cost_factors"].get(
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

                    # Service description and ID
                    service_id = service_name.lower().replace(' ', '-')
                    service_description = service_name

                    # Create or reuse resource names
                    if service_name not in resource_names or region not in resource_names[service_name]:
                        resource_names[service_name][region] = []

                        # Generate resources based on settings
                        num_resources = DATA_VOLUME_SETTINGS["max_resources_per_service"]
                        for _ in range(num_resources):
                            machine_type = None
                            if "machine_types" in service_details and service_details["machine_types"]:
                                machine_type = random.choice(
                                    service_details["machine_types"])

                            # For compute resources, also pick a zone
                            zone = None
                            if service_name == "ComputeEngine":
                                zone = f"{region}-{random.choice(['a', 'b', 'c'])}"

                            resource_name = generate_resource_name(
                                service_name, project_display_name, region, zone, machine_type)
                            resource_names[service_name][region].append({
                                "name": resource_name,
                                "machine_type": machine_type,
                                "zone": zone,
                                "project_id": project_id,
                                "project_display_name": project_display_name
                            })

                            # Generate enhanced labels for this resource
                            labels = generate_resource_labels(
                                resource_name,
                                service_name,
                                project_name,
                                project_data,
                                stage_name,
                                machine_type
                            )
                            labels_data.extend(labels)

                    # Distribute budget across resources
                    num_resources = len(resource_names[service_name][region])
                    resource_budget = region_budget / num_resources if num_resources > 0 else 0

                    for resource_data in resource_names[service_name][region]:
                        resource_name = resource_data["name"]
                        machine_type = resource_data["machine_type"]
                        zone = resource_data["zone"]

                        if resource_budget <= 0:
                            continue

                        # Generate usage records based on settings
                        num_usage_records = random.randint(
                            1, DATA_VOLUME_SETTINGS["max_usage_records_per_day"])

                        for _ in range(num_usage_records):
                            # Determine cost type (regular, tax, adjustment, etc.)
                            cost_type = random.choices(
                                COST_TYPES, weights=COST_TYPE_WEIGHTS)[0]

                            # Determine usage amount, rate, and cost
                            base_rate = service_details.get("base_rate", 0.01)

                            # Apply some randomness to the rate
                            rate_variability = random.uniform(0.9, 1.1)
                            rate = base_rate * rate_variability

                            # Get unit for this service
                            unit = service_details.get("unit", "hour")

                            # Standard pricing unit (may differ from usage unit)
                            pricing_unit = unit

                            # Calculate effective price (after discounts)
                            effective_price = calculate_effective_price(
                                service_name, project_id, rate)

                            # Calculate usage amount based on budget and effective price
                            usage_amount = resource_budget / effective_price / \
                                num_usage_records if effective_price > 0 else 0

                            # Amount in pricing units (sometimes differs from usage amount)
                            # For simplicity, we'll set them equal for most cases
                            amount_in_pricing_units = usage_amount

                            # Calculate cost
                            cost = usage_amount * effective_price

                            # For special cost types
                            if cost_type == "tax":
                                # Tax is typically a percentage of the cost
                                usage_amount = 1.0
                                tax_rate = resource_budget * 0.1 / num_usage_records  # 10% tax
                                cost = tax_rate
                                effective_price = tax_rate
                                amount_in_pricing_units = 1.0

                            elif cost_type == "adjustment":
                                # Adjustments can be credits or additional charges
                                adjustment_sign = 1 if random.random() < 0.3 else -1  # 70% are credits (negative)
                                adjustment_percent = random.uniform(
                                    0.05, 0.2)  # 5-20% adjustment
                                cost = adjustment_sign * resource_budget * \
                                    adjustment_percent / num_usage_records
                                usage_amount = 1.0
                                amount_in_pricing_units = 1.0
                                effective_price = cost  # For adjustments, price equals cost

                            elif cost_type == "rounding_error":
                                # Small rounding errors
                                cost = random.uniform(
                                    0.0001, 0.001) * (1 if random.random() < 0.5 else -1)
                                usage_amount = 1.0
                                amount_in_pricing_units = 1.0
                                effective_price = cost

                            # Choose a random operation and SKU from service details
                            operations = service_details.get(
                                "operations", ["Default"])
                            operation = random.choice(operations)

                            # SKU ID and description
                            sku_ids = service_details.get(
                                "sku_ids", ["00000000-0000"])
                            sku_id = random.choice(sku_ids)

                            # Generate SKU description using pattern
                            sku_name_pattern = service_details.get(
                                "sku_name_pattern", "{service} {operation} in {region}")
                            sku_description = sku_name_pattern.format(
                                service=service_name,
                                operation=operation,
                                region=region
                            )

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

                            # Format in ISO 8601 format (GCP style)
                            usage_start_time = usage_start.strftime(
                                '%Y-%m-%dT%H:%M:%S%z')
                            usage_end_time = usage_end.strftime(
                                '%Y-%m-%dT%H:%M:%S%z')

                            # Export time (when the billing record was generated)
                            export_time = (
                                usage_end + datetime.timedelta(hours=random.randint(1, 4))).strftime('%Y-%m-%dT%H:%M:%S%z')

                            # Invoice month (YYYY-MM format)
                            invoice_month = f"{current_date.year}-{current_date.month:02d}"

                            # Generate system labels based on service
                            system_labels = generate_system_labels(
                                service_name, resource_name, project_id,
                                region, zone, machine_type)

                            # Generate project labels dictionary
                            project_labels = {}
                            for label in labels_data:
                                if label["resource_name"] == resource_name:
                                    project_labels[label["key"]
                                                   ] = label["value"]

                            # Generate credits if applicable
                            credits_info = generate_credits(
                                service_name, cost, project_id)

                            # Create adjustment info if this is an adjustment
                            adjustment_info = None
                            if cost_type == "adjustment":
                                adjustment_type = "USAGE_CORRECTION" if cost > 0 else "CREDIT_ADJUSTMENT"
                                adjustment_info = {
                                    "id": f"adj-{uuid.uuid4().hex[:8]}",
                                    "description": f"{adjustment_type} for {service_name} usage in {region}",
                                    "mode": adjustment_type
                                }

                            # Location information
                            location_info = {
                                "location": region,
                                "country": "US",  # Simplified - would vary by region
                                "region": region,
                                "zone": zone
                            }

                            # Generate tiered price information
                            tiered_rates = generate_tiered_rates(
                                service_name, unit, effective_price)

                            # Price tier information
                            price_info = {
                                "effective_price": effective_price,
                                "tier": "Standard",
                                "tiered_rates": tiered_rates
                            }

                            # Project ancestry for organizational structure
                            project_ancestry = f"organizations/{CONFIG['organization_structure']['Organization']['org_id']}"
                            if "BusinessUnits" in stage_name:
                                project_ancestry += f"/folders/{CONFIG['organization_structure']['Organization']['folders']['BusinessUnits']['folder_id']}"

                            # Create the record
                            record = {
                                "billing_account_id": billing_account_id,
                                "service.id": service_id,
                                "service.description": service_description,
                                "sku.id": sku_id,
                                "sku.description": sku_description,
                                "usage_start_time": usage_start_time,
                                "usage_end_time": usage_end_time,
                                "project.id": project_id,
                                "project.number": project_number,
                                "project.name": project_display_name,
                                "project.ancestry_numbers": project_ancestry,
                                "project.labels": json.dumps(project_labels),
                                "location.location": location_info["location"],
                                "location.country": location_info["country"],
                                "location.region": location_info["region"],
                                "location.zone": location_info["zone"],
                                "export_time": export_time,
                                "cost": cost,
                                "currency": CURRENCY_CODE,
                                "currency_conversion_rate": 1.0,  # Assuming no conversion
                                "usage.amount": usage_amount,
                                "usage.unit": unit,
                                "usage.amount_in_pricing_units": amount_in_pricing_units,
                                "usage.pricing_unit": pricing_unit,
                                "credits": json.dumps(credits_info),
                                "invoice.month": invoice_month,
                                "cost_type": cost_type,
                                "adjustment_info.id": adjustment_info["id"] if adjustment_info else "",
                                "adjustment_info.description": adjustment_info["description"] if adjustment_info else "",
                                "adjustment_info.mode": adjustment_info["mode"] if adjustment_info else "",
                                "system_labels": json.dumps(system_labels),
                                "resource.name": resource_name,
                                "resource.global_name": f"//cloudresourcemanager.googleapis.com/projects/{project_id}/services/{service_id}/resources/{resource_name}",
                                "price.effective_price": price_info["effective_price"],
                                "price.tier": price_info["tier"],
                                "price.tiered_rates": json.dumps(price_info["tiered_rates"])
                            }

                            results.append(record)

                            # Subtract from budget for subsequent calculations
                            resource_budget -= cost

    return results, labels_data


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

        results, labels = generate_usage_data(
            project_name, project_data, day_count, start_date, daily_budget)
        end_time = time.time()
        print(
            f"Generated {len(results)} records for project {project_name} in {end_time - start_time:.2f} seconds")
        return results, labels
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


def generate_chargeback_reports(df_records, df_labels, output_dir):
    """Generate chargeback and showback reports based on cost data and labels"""

    # First, merge the labels data with the billing data
    # Extract resource names and convert labels from JSON
    df_records['resource_name'] = df_records['resource.name']

    # Create a mapping of resource names to chargeback entities
    resource_to_entity = {}
    resource_allocation_method = {}

    for _, label in df_labels.iterrows():
        if label['key'] == 'chargeback-entity':
            resource_to_entity[label['resource_name']] = label['value']
        if label['key'] == 'allocation-method':
            resource_allocation_method[label['resource_name']] = label['value']

    # Apply mapping to get chargeback entity for each record
    df_records['chargeback_entity'] = df_records['resource_name'].map(
        resource_to_entity).fillna("Unallocated")

    df_records['allocation_method'] = df_records['resource_name'].map(
        resource_allocation_method).fillna("direct")

    # Convert invoice month to a simpler format
    df_records['month'] = df_records['invoice.month']

    # 1. Direct Chargeback Report - what each entity should be charged
    chargeback_summary = df_records.groupby(['month', 'chargeback_entity'])[
        'cost'].sum().reset_index()
    chargeback_summary.to_csv(
        f"{output_dir}/chargeback_by_entity.csv", index=False)

    # 2. Generate by Service and Entity
    service_entity_summary = df_records.groupby(
        ['month', 'chargeback_entity', 'service.description'])['cost'].sum().reset_index()
    service_entity_summary.to_csv(
        f"{output_dir}/chargeback_by_service_entity.csv", index=False)

    # 3. Credit Impact Analysis
    # Extract credits from the JSON string and calculate their impact
    total_costs = df_records['cost'].sum()

    # 4. Allocation Methods Report
    allocation_summary = df_records.groupby(['month', 'allocation_method'])[
        'cost'].sum().reset_index()
    allocation_summary.to_csv(
        f"{output_dir}/cost_by_allocation_method.csv", index=False)

    return {
        'chargeback_total': chargeback_summary['cost'].sum(),
        'direct_allocation': allocation_summary[allocation_summary['allocation_method'] == 'direct']['cost'].sum(),
        'shared_allocation': allocation_summary[allocation_summary['allocation_method'] != 'direct']['cost'].sum(),
    }


def analyze_discount_impact(df_records, output_dir):
    """Analyze the impact of discounts and credits on costs"""

    # Extract credits from JSON string
    df_records['credits_list'] = df_records['credits'].apply(
        lambda x: json.loads(x) if x and x != '[]' else [])

    # Calculate total credits per record
    df_records['credit_amount'] = df_records['credits_list'].apply(
        lambda credits: sum(credit.get('amount', 0) for credit in credits) if credits else 0)

    # Calculate effective cost after credits
    df_records['effective_cost'] = df_records['cost'] + \
        df_records['credit_amount']

    # Summary by project
    project_summary = df_records.groupby(['project.id', 'project.name'])[
        ['cost', 'credit_amount', 'effective_cost']].sum().reset_index()
    project_summary['discount_percent'] = (project_summary['credit_amount'] /
                                           project_summary['cost'] * 100).fillna(0)
    project_summary.to_csv(
        f"{output_dir}/discount_impact_by_project.csv", index=False)

    # Summary by service
    service_summary = df_records.groupby(['service.description'])[
        ['cost', 'credit_amount', 'effective_cost']].sum().reset_index()
    service_summary['discount_percent'] = (service_summary['credit_amount'] /
                                           service_summary['cost'] * 100).fillna(0)
    service_summary.to_csv(
        f"{output_dir}/discount_impact_by_service.csv", index=False)

    # Find resources with the largest discount amounts
    resource_summary = df_records.groupby(['resource.name'])[
        ['cost', 'credit_amount', 'effective_cost']].sum().reset_index()
    resource_summary = resource_summary.sort_values(
        'credit_amount', ascending=True)  # Ascending because credits are negative
    top_resources = resource_summary.head(20)
    top_resources.to_csv(
        f"{output_dir}/top_discount_impact_resources.csv", index=False)

    # Overall statistics
    total_cost = df_records['cost'].sum()
    total_credits = df_records['credit_amount'].sum()
    total_effective = df_records['effective_cost'].sum()
    percent_discount = (total_credits / total_cost *
                        100) if total_cost > 0 else 0

    summary_stats = {
        'total_cost': total_cost,
        'total_credits': total_credits,
        'total_effective_cost': total_effective,
        'percent_discount': percent_discount,
        'projects_with_discounts': len(project_summary[project_summary['credit_amount'] < 0]),
    }

    # Save summary stats
    with open(f"{output_dir}/discount_impact_summary.json", 'w') as f:
        json.dump(summary_stats, f, indent=2)

    return summary_stats


def main():
    print("GCP Billing Data Generator")
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
            f"WARNING: Found services in projects that are not defined in GCP_SERVICES: {', '.join(missing_services)}")

    # Prepare arguments for parallel processing
    project_args = []
    for proj_name in selected_projects:
        proj_data = CONFIG["projects"].get(proj_name, {})
        project_args.append(
            (proj_name, proj_data, day_count, start_date, daily_budget))

    # Use multiprocessing to generate data in parallel
    all_records = []
    all_labels = []

    with multiprocessing.Pool(processes=min(len(project_args), multiprocessing.cpu_count())) as pool:
        results = pool.map(process_project, project_args)

        for records, labels in results:
            all_records.extend(records)
            all_labels.extend(labels)

    print(
        f"Generated {len(all_records)} total records and {len(all_labels)} labels")

    # Convert to DataFrames
    df_records = pd.DataFrame(all_records)
    df_labels = pd.DataFrame(all_labels)

    # Ensure all columns exist in the DataFrame
    for col in BIGQUERY_EXPORT_COLUMNS:
        if col not in df_records.columns:
            df_records[col] = ""

    for col in RESOURCE_LABELS_COLUMNS:
        if col not in df_labels.columns:
            df_labels[col] = ""

    # Save to CSV
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    df_records.to_csv(f"{output_dir}/gcp_billing_export.csv", index=False)
    df_labels.to_csv(f"{output_dir}/resource_labels.csv", index=False)

    # Save the project lifecycle mapping
    project_lifecycle_df.to_csv(
        f"{output_dir}/project_lifecycle_mapping.csv", index=False)
    print(
        f"Saved project lifecycle mapping to {output_dir}/project_lifecycle_mapping.csv")

    # Generate a summary per project per month
    if not df_records.empty:
        # Extract month from invoice.month column
        df_records['month'] = df_records['invoice.month']

        # Create project summary
        project_summary = df_records.groupby(['month', 'project.name'])[
            'cost'].sum().reset_index()
        project_summary.to_csv(
            f"{output_dir}/cost_summary_by_project.csv", index=False)

        # Generate summary by service
        service_summary = df_records.groupby(['month', 'service.description'])[
            'cost'].sum().reset_index()
        service_summary.to_csv(
            f"{output_dir}/cost_summary_by_service.csv", index=False)

        # Map project names to business units
        project_to_bu = {}
        for project_name in selected_projects:
            project_data = CONFIG["projects"].get(project_name, {})
            project_to_bu[project_name] = project_data.get(
                "business_unit", "Unknown")

        # Create a mapping from project.name to business unit
        project_name_to_bu = {}
        for project_name, bu in project_to_bu.items():
            # Convert project name to the format in project.name
            for record in df_records['project.name'].unique():
                if project_name.lower() in record.lower():
                    project_name_to_bu[record] = bu

        # Apply mapping to get business unit
        df_records['business_unit'] = df_records['project.name'].map(
            project_name_to_bu).fillna("Unknown")

        # Generate monthly cost summary by business unit
        bu_summary = df_records.groupby(['month', 'business_unit'])[
            'cost'].sum().reset_index()
        bu_summary.to_csv(
            f"{output_dir}/cost_summary_by_business_unit.csv", index=False)

        # Generate chargeback/showback reports
        chargeback_stats = generate_chargeback_reports(
            df_records, df_labels, output_dir)
        print(
            f"Generated chargeback/showback reports. Total chargeback: ${chargeback_stats['chargeback_total']:.2f}")

        # Analyze discount impact
        discount_impact = analyze_discount_impact(df_records, output_dir)
        print(f"Analyzed discount impact. Total credits: ${discount_impact['total_credits']:.2f} " +
              f"({discount_impact['percent_discount']:.2f}%)")

    end_time = time.time()
    print(f"Generated GCP billing data in {end_time - start_time:.2f} seconds")
    print(f"Data saved to {output_dir}/")


if __name__ == "__main__":
    main()
