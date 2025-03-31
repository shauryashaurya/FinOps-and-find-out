import numpy as np
import pandas as pd
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
from configAzure import CONFIG


def get_azure_offer_id(subscription_id, subscription_name):
    """Generate a realistic Azure offer ID based on subscription details"""
    # Common Azure offer IDs
    offer_ids = {
        "enterprise": "MS-AZR-0017P",      # Enterprise Agreement
        "free_trial": "MS-AZR-0044P",      # Free Trial
        "pay_as_you_go": "MS-AZR-0003P",   # Pay-As-You-Go
        "dev_test": "MS-AZR-0148P",        # Dev/Test Pay-As-You-Go
        "msdn": "MS-AZR-0063P",            # MSDN
        "csp": "MS-AZR-0145P",             # CSP
        "student": "MS-AZR-0170P",         # Azure for Students
    }

    # Select offer based on subscription characteristics
    if "Development" in subscription_name or "dev" in subscription_name.lower():
        if random.random() < 0.7:
            return offer_ids["dev_test"]
        else:
            return offer_ids["msdn"]
    elif "Research" in subscription_name:
        if random.random() < 0.6:
            return offer_ids["msdn"]
        else:
            return offer_ids["enterprise"]
    elif "Sandbox" in subscription_name:
        if random.random() < 0.5:
            return offer_ids["free_trial"]
        else:
            return offer_ids["dev_test"]
    elif "Production" in subscription_name or "prod" in subscription_name.lower():
        # Production workloads typically use Enterprise or Pay-As-You-Go
        if random.random() < 0.8:
            return offer_ids["enterprise"]
        else:
            return offer_ids["pay_as_you_go"]
    else:
        # Default to enterprise for most other cases
        return offer_ids["enterprise"]


def generate_cost_allocation_rule(resource_id, resource_tags):
    """Generate cost allocation rule information based on resource tags"""
    # If the resource doesn't have allocation tags, return empty string
    allocation_method = None
    for tag in resource_tags:
        if tag["resource_id"] == resource_id and tag["key"] == "allocation-method":
            allocation_method = tag["value"]
            break

    if not allocation_method:
        return ""

    # Generate a rule name based on the allocation method
    if allocation_method == "equal":
        return "EqualSplit-SharedServices"
    elif allocation_method == "proportional":
        return "ProportionalUsage-ITServices"
    elif allocation_method == "direct":
        return ""
    elif allocation_method == "tiered":
        return "TieredConsumption-EnterpriseShared"
    else:
        # Find all allocation percentage tags for this resource
        allocation_entities = []
        for tag in resource_tags:
            if tag["resource_id"] == resource_id and tag["key"].startswith("allocation-") and tag["key"] != "allocation-method":
                entity = tag["key"].replace("allocation-", "")
                allocation_entities.append(entity)

        if allocation_entities:
            return f"Custom-{'-'.join(sorted(allocation_entities)[:2])}"
        else:
            return "CustomAllocation"


def generate_tiered_rates(service_name, unit, effective_price):
    """Generate realistic tiered rates for services with tiered pricing"""

    # Services commonly using tiered pricing
    tiered_services = {
        "BlobStorage": {
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
        "SynapseAnalytics": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1,
                    "unit_price": effective_price * 1.0},      # First 1TB
                {"start_usage_amount": 1, "end_usage_amount": 10,
                    "unit_price": effective_price * 0.85},    # Next 9TB
                {"start_usage_amount": 10, "end_usage_amount": None,
                    "unit_price": effective_price * 0.65}  # Over 10TB
            ]
        },
        "LogAnalytics": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 50,
                    "unit_price": 0.0},               # First 50GB free
                {"start_usage_amount": 50, "end_usage_amount": 100,
                    "unit_price": effective_price * 0.9},  # Next 50GB
                {"start_usage_amount": 100, "end_usage_amount": None,
                    "unit_price": effective_price}       # Over 100GB
            ]
        },
        "VirtualMachines": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.7}  # Reserved Instance discount
            ]
        },
        "Functions": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1000000,
                    "unit_price": 0.0},                 # First 1M executions free
                {"start_usage_amount": 1000000, "end_usage_amount": None,
                    "unit_price": effective_price}   # Over 1M executions
            ]
        },
        "ContainerInstances": {
            "tiers": [
                # First 180K seconds free
                {"start_usage_amount": 0, "end_usage_amount": 180000, "unit_price": 0.0},
                {"start_usage_amount": 180000, "end_usage_amount": None,
                    "unit_price": effective_price}    # Over 180K seconds
            ]
        },
        "EventHubs": {
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
        "DataFactory": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 5000,
                    "unit_price": effective_price},          # First 5000 runs
                {"start_usage_amount": 5000, "end_usage_amount": 10000,
                    "unit_price": effective_price * 0.95},  # 5000-10000 runs
                {"start_usage_amount": 10000, "end_usage_amount": None,
                    "unit_price": effective_price * 0.9}  # Over 10000 runs
            ]
        },
        "CosmosDB": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 100,
                    "unit_price": effective_price},           # 0-100 RU/s
                {"start_usage_amount": 100, "end_usage_amount": 1000,
                    "unit_price": effective_price * 0.9},   # 100-1000 RU/s
                {"start_usage_amount": 1000, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Over 1000 RU/s
            ]
        },
        "Monitor": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 5,
                    "unit_price": 0.0},                      # First 5GB free
                {"start_usage_amount": 5, "end_usage_amount": 100,
                    "unit_price": effective_price},     # 5GB-100GB
                {"start_usage_amount": 100, "end_usage_amount": None,
                    "unit_price": effective_price * 0.6}  # Over 100GB
            ]
        },
        "VirtualNetwork": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 1,
                    "unit_price": 0.0},                         # First 1GB free
                {"start_usage_amount": 1, "end_usage_amount": 1024,
                    "unit_price": effective_price},         # 1GB-1TB
                {"start_usage_amount": 1024, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Over 1TB
            ]
        },
        "SQLDatabase": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.7}  # Reserved Instance discount
            ]
        },
        "AKS": {
            "tiers": [
                {"start_usage_amount": 0, "end_usage_amount": 730,
                    "unit_price": effective_price},         # First 730 hours
                {"start_usage_amount": 730, "end_usage_amount": None,
                    "unit_price": effective_price * 0.8}  # Reserved Instance discount
            ]
        },
        "CDN": {
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
    "maximum_projects_to_be_picked": 11,
    "days_to_generate": 512,                  # Number of days to generate data for
    "sampling_interval": 3,                   # Generate data every X days
    "max_services_per_project": 78,            # Limit number of services per project
    "max_resources_per_service": 3,           # Number of resources per service
    # Max usage records per day per resource
    "max_usage_records_per_day": 3,
    "primary_regions_per_project": 1,         # Number of primary regions
    "dr_region_probability": 0.2,             # Probability of using DR region
    "volatility_factor": 0.02,                # +/- 2% cost volatility by default
}

# Tag categories for more realistic tagging
TAG_CATEGORIES = {
    "Technical": [
        {"key": "name", "values": None},  # Will be set dynamically
        {"key": "environment", "values": [
            "production", "development", "testing", "staging", "qa", "uat", "dr"]},
        {"key": "version", "values": [
            "1.0", "2.0", "3.0", "latest", "stable", "beta"]},
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
            "terraform", "arm-template", "bicep", "portal", "az-cli", "api"]},
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

# Service-specific tags
SERVICE_SPECIFIC_TAGS = {
    "VirtualMachines": [
        {"key": "vm-size", "values": None},  # Will be set dynamically
        {"key": "image", "values": [
            "ubuntu-20.04", "windows-2019", "rhel-8", "debian-10", "centos-7"]},
        {"key": "auto-shutdown", "values": [
            "true", "false", "weekends", "nights"]},
        {"key": "patch-group", "values": [
            "group1", "group2", "critical", "standard", "dev"]},
    ],
    "BlobStorage": [
        {"key": "access-tier", "values": [
            "hot", "cool", "archive"]},
        {"key": "encryption", "values": [
            "microsoft-managed", "customer-managed"]},
        {"key": "public-access", "values": [
            "none", "blob", "container"]},
        {"key": "lifecycle-policy", "values": [
            "30-day-cool", "90-day-archive", "1-year-delete", "compliance-7-years"]},
    ],
    "SQLDatabase": [
        {"key": "engine", "values": [
            "sql", "mysql", "postgresql", "mariadb"]},
        {"key": "ha-enabled", "values": ["true", "false"]},
        {"key": "backup-retention", "values": ["7", "14", "30", "90"]},
        {"key": "db-name", "values": ["prod-db",
                                      "dev-db", "test-db", "analytics-db"]},
    ],
    "Functions": [
        {"key": "runtime", "values": [
            "dotnet-6", "node14", "node16", "python3.9", "python3.10", "java11"]},
        {"key": "plan-type",
            "values": ["consumption", "premium", "dedicated"]},
        {"key": "timeout", "values": ["5", "10", "20", "30"]},
        {"key": "trigger-type", "values": [
            "http", "blob", "eventgrid", "eventhub", "timer"]},
    ],
    "CosmosDB": [
        {"key": "api", "values": [
            "sql", "mongodb", "cassandra", "table", "gremlin"]},
        {"key": "consistency-level",
            "values": ["strong", "bounded-staleness", "session", "consistent-prefix", "eventual"]},
        {"key": "multi-region", "values": [
            "true", "false"]},
        {"key": "free-tier", "values": ["true", "false"]},
    ],
    "ManagedDisks": [
        {"key": "disk-type", "values": [
            "standard-hdd", "standard-ssd", "premium-ssd", "ultra-disk"]},
        {"key": "encrypted", "values": [
            "microsoft-managed", "customer-managed"]},
        {"key": "snapshot-schedule", "values": [
            "daily", "weekly", "monthly", "none"]},
        {"key": "delete-with-vm", "values": ["true", "false"]},
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
        "services": ["VirtualNetwork", "ExpressRoute", "DNSZones", "LogAnalytics", "DefenderForCloud"]
    },
    "data_services": {
        "model": "direct",
        "allocation_key": "data_volume",
        "entities": ["Analytics", "DataScience", "ProductDevelopment"],
        "services": ["BlobStorage", "SQLDatabase", "CosmosDB", "SynapseAnalytics", "DataFactory"]
    },
    "security_compliance": {
        "model": "equal",
        "allocation_key": None,
        "entities": ["IT", "SecurityOperations", "Compliance", "Legal", "Finance"],
        "services": ["DefenderForCloud", "ActiveDirectory", "KeyVault", "DDoSProtection", "DefenderForCloud"]
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

# Reserved Instance (RI) and Savings Plan benefit mapping for effective cost simulation
BENEFIT_DISCOUNT_MAPPING = {
    "VirtualMachines": {
        # Mapping subscriptions to discount factors
        # Values <1 indicate discount (subscription owns RIs)
        # Values >1 indicate paying the premium (subscription uses shared resources)
        # Shared services with 30% RI discount
        "00000000-0000-0000-0000-000000666666": 0.7,
        "00000000-0000-0000-0000-000000555555": 0.85,   # Security with 15% RI discount
        "00000000-0000-0000-0000-000222200001": 1.05,   # Aviation Dev pays 5% more
        # Aviation Prod gets 10% RI discount
        "00000000-0000-0000-0000-000444400001": 0.9,
    },
    "SQLDatabase": {
        # Shared services with 25% RI discount
        "00000000-0000-0000-0000-000000666666": 0.75,
        "00000000-0000-0000-0000-000444400002": 0.95,    # Pharma Prod with 5% RI discount
    },
    "AKS": {
        # Shared services with 20% Savings Plan discount
        "00000000-0000-0000-0000-000000666666": 0.8,
    },
    "Functions": {
        # SoftwareSolutions Prod with 10% Savings Plan discount
        "00000000-0000-0000-0000-000444400005": 0.9,
    }
}

# Azure Cost Management Schema columns
# Based on Azure Cost Management Export schema
COST_MANAGEMENT_COLUMNS = [
    "BillingAccountId",
    "BillingAccountName",
    "BillingPeriodStartDate",
    "BillingPeriodEndDate",
    "BillingProfileId",
    "BillingProfileName",
    "AccountOwnerId",
    "AccountName",
    "SubscriptionId",
    "SubscriptionName",
    "Date",
    "Product",
    "PartNumber",
    "MeterId",
    "ServiceFamily",
    "MeterCategory",
    "MeterSubCategory",
    "MeterName",
    "MeterRegion",
    "UnitOfMeasure",
    "Quantity",
    "EffectivePrice",
    "Cost",
    "CostInBillingCurrency",
    "CostCenter",
    "ResourceLocation",
    "ConsumedService",
    "ResourceId",
    "ResourceName",
    "ServiceName",
    "ServiceTier",
    "ResourceGroupName",
    "ResourceType",
    "PublisherType",
    "PublisherName",
    "ReservationId",
    "ReservationName",
    "ProductOrderId",
    "ProductOrderName",
    "OfferId",
    "BenefitId",
    "BenefitName",
    "Term",
    "CostAllocationRuleName",
    "Tags",
    "AdditionalInfo",
    "ServiceInfo1",
    "ServiceInfo2",
    "PricingModel",
    "ChargeType",
    "Frequency",
    "PricingCurrency"
]

# Resource Tags columns
RESOURCE_TAGS_COLUMNS = [
    "resource_id",
    "key",
    "value"
]


def calculate_daily_budget():
    """Calculate daily budget from annual budget"""
    annual_budget = CONFIG["annual_budget"]
    daily_budget = annual_budget / 365.0
    return daily_budget


def get_subscription_details(stage_name):
    """Find subscription ID, and name for a given stage name"""
    # Use direct mapping from config if available
    stage_map = CONFIG.get("STAGE_TO_SUBSCRIPTION_MAPPING", {})

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

    # Create a deterministic subscription ID based on the stage name
    # This ensures consistent IDs for the same stage names across runs
    stage_hash = hashlib.md5(stage_name_normalized.encode()).hexdigest()[:8]

    # Format subscription name nicely
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

    subscription_name = f"{business_unit} {' '.join(formatted_parts)}"
    subscription_id = f"00000000-0000-0000-0000-{stage_hash.ljust(12, '0')}"

    return {
        "subscription_id": subscription_id,
        "subscription_name": subscription_name
    }


def get_billing_account_for_subscription(subscription_name):
    """Get the billing account ID for a subscription"""
    subscription_billing_mapping = CONFIG["subscription_billing_mapping"]
    billing_accounts = CONFIG["billing_accounts"]

    # Normalize subscription name for matching
    subscription_name_normalized = subscription_name.lower().replace('_', '-')

    # Try exact match first
    if subscription_name in subscription_billing_mapping:
        billing_key = subscription_billing_mapping[subscription_name]
        return billing_accounts[billing_key]["id"]

    # Try normalized match
    for mapping_name, billing_key in subscription_billing_mapping.items():
        mapping_normalized = mapping_name.lower().replace('_', '-')

        # Check if either name contains the other
        if mapping_normalized in subscription_name_normalized or subscription_name_normalized in mapping_normalized:
            return billing_accounts[billing_key]["id"]

    # Check for specific environments in the subscription name
    if "dev" in subscription_name_normalized or "sandbox" in subscription_name_normalized:
        return billing_accounts["development"]["id"]
    elif "research" in subscription_name_normalized:
        return billing_accounts["research"]["id"]

    # Default to primary billing account
    return billing_accounts["primary"]["id"]


def generate_resource_name(service_name, project_name, region=None, vm_size=None):
    """Generate a realistic Azure resource name based on service type"""
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

    # Generate names based on Azure naming conventions
    if service_name == "VirtualMachines":
        # Virtual Machine naming convention
        purpose = random.choice(
            ['web', 'app', 'db', 'api', 'worker', 'batch', 'test'])
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        if vm_size:
            # Size indicator (e.g., 's' for small)
            size = vm_size.split('_')[-1][0].lower()
        else:
            size = random.choice(['s', 'm', 'l', 'xl'])

        return f"{project_prefix}-{purpose}-{env}-{size}-{unique_id[:4]}"

    elif service_name == "BlobStorage":
        # Storage account naming convention (lowercase, 3-24 chars, alphanumeric)
        purpose = random.choice(
            ['data', 'backup', 'archive', 'media', 'logs'])

        # Generate unique name suitable for global namespace
        # Azure storage accounts must be globally unique and 3-24 chars
        return f"{project_prefix}{purpose}{unique_id[:8]}".lower()[:24]

    elif service_name == "SQLDatabase":
        # SQL Database naming convention
        db_type = random.choice(['sql', 'mysql', 'postgres', 'mariadb'])
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        return f"{project_prefix}-{db_type}-{env}-{unique_id[:4]}"

    elif service_name == "Functions":
        # Functions naming convention
        purpose = random.choice(
            ['func', 'process', 'api', 'auth', 'notify', 'schedule', 'trigger'])
        return f"{project_prefix}-{purpose}-{unique_id[:4]}"

    elif service_name == "CosmosDB":
        # CosmosDB account naming convention (lowercase, 3-44 chars)
        purpose = random.choice(['doc', 'graph', 'nosql', 'data'])
        return f"{project_prefix}-{purpose}-{unique_id[:4]}".lower()

    elif service_name == "ManagedDisks":
        # Managed Disk naming convention
        disk_type = random.choice(['osdisk', 'datadisk'])
        purpose = random.choice(['boot', 'data', 'temp', 'swap', 'cache'])
        return f"{project_prefix}-{disk_type}-{purpose}-{unique_id[:4]}"

    elif service_name == "CDN":
        # CDN profile naming convention
        return f"{project_prefix}-cdn-{unique_id[:4]}"

    elif service_name == "SynapseAnalytics":
        # Synapse workspace naming convention
        purpose = random.choice(
            ['syn', 'analytics', 'dw', 'insight'])
        return f"{project_prefix}{purpose}{unique_id[:8]}".lower()[:24]

    elif service_name == "AKS":
        # AKS cluster naming convention
        env = 'prod' if 'prod' in project_name.lower(
        ) else 'dev' if 'dev' in project_name.lower() else 'test'
        return f"{project_prefix}-{env}-aks-{unique_id[:4]}"

    elif service_name == "ContainerInstances":
        # Container Instance naming convention
        purpose = random.choice(
            ['ci', 'container', 'task', 'job'])
        return f"{project_prefix}-{purpose}-{unique_id[:4]}"

    else:
        # Generic naming for other services
        service_short = ''.join(
            [word[0] for word in service_name.split() if word]).lower()
        if len(service_short) < 2:
            service_short = service_name[:3].lower()

        return f"{project_prefix}-{service_short}-{unique_id[:4]}"


def generate_resource_id(subscription_id, resource_name, service_name, resource_group_name=None):
    """Generate a valid Azure Resource ID"""
    # If no resource group provided, generate one
    if not resource_group_name:
        # Extract prefix from resource name
        parts = resource_name.split('-')
        if len(parts) >= 2:
            prefix = parts[0]
        else:
            prefix = resource_name[:3]

        resource_group_name = f"{prefix}-rg"

    # Get resource type path based on service name
    resource_type = get_resource_type_path(service_name)

    # Construct resource ID
    return f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_type}/{resource_name}"


def get_resource_type_path(service_name):
    """Map service name to Azure resource provider path"""
    # Map service names to Azure Resource Manager resource types
    resource_types = {
        "VirtualMachines": "Microsoft.Compute/virtualMachines",
        "ManagedDisks": "Microsoft.Compute/disks",
        "BlobStorage": "Microsoft.Storage/storageAccounts",
        "Files": "Microsoft.Storage/storageAccounts/fileServices/shares",
        "SQLDatabase": "Microsoft.Sql/servers/databases",
        "CosmosDB": "Microsoft.DocumentDB/databaseAccounts",
        "Redis": "Microsoft.Cache/Redis",
        "EventHubs": "Microsoft.EventHub/namespaces",
        "ServiceBus": "Microsoft.ServiceBus/namespaces",
        "Functions": "Microsoft.Web/sites/functions",
        "AppService": "Microsoft.Web/sites",
        "AKS": "Microsoft.ContainerService/managedClusters",
        "ContainerInstances": "Microsoft.ContainerInstance/containerGroups",
        "SynapseAnalytics": "Microsoft.Synapse/workspaces",
        "DataFactory": "Microsoft.DataFactory/factories",
        "HDInsight": "Microsoft.HDInsight/clusters",
        "VirtualNetwork": "Microsoft.Network/virtualNetworks",
        "LoadBalancer": "Microsoft.Network/loadBalancers",
        "VPNGateway": "Microsoft.Network/virtualNetworkGateways",
        "ExpressRoute": "Microsoft.Network/expressRouteCircuits",
        "NATGateway": "Microsoft.Network/natGateways",
        "CDN": "Microsoft.Cdn/profiles",
        "DNSZones": "Microsoft.Network/dnszones",
        "DDoSProtection": "Microsoft.Network/ddosProtectionPlans",
        "MachineLearning": "Microsoft.MachineLearningServices/workspaces",
        "OpenAI": "Microsoft.CognitiveServices/accounts",
        "CognitiveServices": "Microsoft.CognitiveServices/accounts",
        "BotService": "Microsoft.BotService/botServices",
        "Monitor": "Microsoft.OperationalInsights/workspaces",
        "LogAnalytics": "Microsoft.OperationalInsights/workspaces",
        "ApplicationInsights": "Microsoft.Insights/components",
        "CostManagement": "Microsoft.CostManagement/reports",
        "ManagedGrafana": "Microsoft.Dashboard/grafana",
        "DevOps": "Microsoft.DevOps/pipelines",
        "ARM": "Microsoft.Resources/deployments",
        "KeyVault": "Microsoft.KeyVault/vaults",
        "DefenderForCloud": "Microsoft.Security/securitySolutions",
        "ActiveDirectory": "Microsoft.AAD/domainServices",
        "DedicatedHSM": "Microsoft.HardwareSecurityModules/dedicatedHSMs",
        "IoTHub": "Microsoft.Devices/IotHubs",
        "IoTCentral": "Microsoft.IoTCentral/IoTApps",
        "IoTEdge": "Microsoft.Devices/provisioningServices",
        "MediaServices": "Microsoft.Media/mediaservices",
        "LiveVideo": "Microsoft.Media/liveEvents",
        "VideoIndexer": "Microsoft.VideoIndexer/accounts",
        "Maps": "Microsoft.Maps/accounts",
        "PowerBI": "Microsoft.PowerBI/workspaces",
        "ElasticSearch": "Microsoft.Elastic/monitors",
        "Logic Apps": "Microsoft.Logic/workflows",
        "API Management": "Microsoft.ApiManagement/service",
        "Service Fabric": "Microsoft.ServiceFabric/clusters",
        "App Configuration": "Microsoft.AppConfiguration/configurationStores",
        "Batch": "Microsoft.Batch/batchAccounts",
        "ArcEnabledServers": "Microsoft.HybridCompute/machines",
        "HealthDataServices": "Microsoft.HealthcareApis/services"
    }

    # Return the resource type or a default if not found
    return resource_types.get(service_name, f"Microsoft.Resources/generic/{service_name}")


def generate_tags(service_name, resource_name, project_name, project_data, stage, vm_size=None):
    """
    Generate rich, realistic tags for Azure resources

    Args:
        resource_name: The Azure resource name
        service_name: Azure service name
        project_name: Project name
        project_data: Project data dictionary
        stage: Deployment stage
        vm_size: VM size (if applicable)

    Returns:
        Dictionary of tags
    """
    tags = {}

    # Common mandatory tags
    business_unit = project_data.get("business_unit", "")
    project_use_case = project_data.get("use_case", "")
    env_type = "production" if "prod" in stage.lower() else "non-production"

    # Base tags that should be on every resource
    base_tags = {
        "name": f"{project_name}-{service_name}",
        "project": project_name,
        "business-unit": business_unit,
        "environment": env_type,
        "cost-center": f"{business_unit}-{random.randint(1000, 9999)}",
    }
    tags.update(base_tags)

    # Add more dynamic base tags
    if project_use_case:
        tags["use-case"] = project_use_case

    # Determine how many tags from each category to add for this resource
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
    if service_name in ["SQLDatabase", "CosmosDB", "BlobStorage"]:
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
            if key in tags:
                continue

            # Determine value
            if tag_spec["values"] is None:
                # Dynamic values
                if key == "name":
                    value = f"{project_name}-{service_name}-{random.randint(1, 999)}"
                elif key == "cost-center":
                    value = f"{business_unit}-{random.randint(1000, 9999)}"
                else:
                    value = "unknown"
            else:
                # Randomly select from provided values
                value = random.choice(tag_spec["values"])

            tags[key] = value

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
            if key in tags:
                continue

            # Determine value
            if tag_spec["values"] is None:
                # Dynamic values
                if key == "vm-size" and vm_size:
                    value = vm_size
                else:
                    value = "default"
            else:
                # Randomly select from provided values
                value = random.choice(tag_spec["values"])

            tags[key] = value

    # Add region consistency - consistent service tags across regions for the same service
    if random.random() < 0.8:  # 80% chance of having consistent service metadata
        tags["service-tier"] = f"{service_name.lower()}-{random.choice(['standard', 'premium', 'basic', 'enterprise'])}"

    # Random team tag
    if random.random() < 0.6:
        tags["team"] = random.choice([
            "devops", "platform", "infrastructure", "application",
            "data-engineering", "analytics", "sre", "security"
        ])

    # Add chargeback tags
    chargeback_tags = generate_chargeback_tags(
        resource_name, service_name, project_name, project_data, stage)
    tags.update(chargeback_tags)

    return tags


def generate_chargeback_tags(resource_name, service_name, project_name, project_data, stage_name):
    """Generate tags related to chargeback/showback models"""
    business_unit = project_data.get("business_unit", "")
    chargeback_tags = {}

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
    chargeback_tags["cost-allocation"] = "direct" if not is_shared_resource else "shared"

    # Add more specific chargeback information for shared resources
    if is_shared_resource:
        allocation_model = "unknown"
        for rule_name, rule_data in COST_ALLOCATION_RULES.items():
            if service_name in rule_data["services"]:
                allocation_model = rule_data["model"]
                break

        chargeback_tags["allocation-method"] = allocation_model

        if shared_resource_id in SHARED_RESOURCE_ALLOCATIONS:
            # Encode the actual allocation percentages - use simplified values
            # Azure tags don't allow complex values like JSON
            for entity, percentage in SHARED_RESOURCE_ALLOCATIONS[shared_resource_id].items():
                chargeback_tags[f"allocation-{entity.lower()}"] = str(
                    int(percentage * 100))

    # Add department-specific tags
    department = chargeback_tags.get("department")
    if department:
        chargeback_tags["chargeback-entity"] = department
    else:
        chargeback_tags["chargeback-entity"] = business_unit

    # Add showback-specific flags
    if "prod" in stage_name.lower():
        chargeback_tags["showback-category"] = "production"
    else:
        chargeback_tags["showback-category"] = "non-production"

    return chargeback_tags


def calculate_effective_price(service_name, subscription_id, base_price):
    """
    Calculate effective price for a given service and subscription,
    taking into account Reserved Instances and Savings Plans
    """
    effective_price = base_price

    # Apply service-specific benefit discount factors if applicable
    if service_name in BENEFIT_DISCOUNT_MAPPING:
        service_discounts = BENEFIT_DISCOUNT_MAPPING[service_name]

        if subscription_id in service_discounts:
            # Apply the discount factor to the base price
            discount_factor = service_discounts[subscription_id]
            effective_price = base_price * discount_factor

    return effective_price


def generate_benefits(service_name, cost, subscription_id):
    """Generate benefit information if applicable"""
    benefits = []

    # Only generate benefit information for certain conditions
    # Reserved Instances, Savings Plans, Azure Hybrid Benefit
    if cost > 10 and random.random() < 0.3:  # 30% chance for high-cost items
        benefit_types = [
            {
                "name": "Reserved Instance",
                "id": f"RI-{uuid.uuid4().hex[:8]}",
                "full_name": "Reserved Instance: 1 year",
                "term": "P1Y",
                "order_id": f"RI-Order-{uuid.uuid4().hex[:6]}",
                "order_name": "Annual Reserved Instance Purchase"
            },
            {
                "name": "Reserved Instance",
                "id": f"RI-{uuid.uuid4().hex[:8]}",
                "full_name": "Reserved Instance: 3 year",
                "term": "P3Y",
                "order_id": f"RI-Order-{uuid.uuid4().hex[:6]}",
                "order_name": "Three Year Reserved Instance Purchase"
            },
            {
                "name": "Savings Plan",
                "id": f"SP-{uuid.uuid4().hex[:8]}",
                "full_name": "Compute Savings Plan",
                "term": "P1Y",
                "order_id": f"SP-Order-{uuid.uuid4().hex[:6]}",
                "order_name": "Annual Compute Savings Plan"
            },
            {
                "name": "Hybrid Benefit",
                "id": f"AHB-{uuid.uuid4().hex[:8]}",
                "full_name": "Azure Hybrid Benefit",
                "term": "",
                "order_id": "",
                "order_name": ""
            }
        ]

        # Certain services are more likely to have specific benefits
        if service_name == "VirtualMachines":
            # VMs commonly use RIs or AHB
            benefit_options = [0, 1, 3]  # Indices of RI 1yr, RI 3yr, AHB
            weights = [0.4, 0.3, 0.3]  # More weight to RIs
        elif service_name == "SQLDatabase":
            # SQL often uses AHB
            benefit_options = [0, 3]  # Indices of RI 1yr and AHB
            weights = [0.3, 0.7]  # More weight to AHB
        elif service_name in ["AKS", "Functions", "ContainerInstances"]:
            # Compute services often use Savings Plans
            benefit_options = [2]  # Index of Savings Plan
            weights = [1.0]
        else:
            # Other services use a mix
            benefit_options = [0, 1, 2, 3]
            weights = [0.3, 0.2, 0.3, 0.2]

        # Weighted selection of benefit type
        selected_index = random.choices(benefit_options,
                                        weights=[weights[i % len(weights)] for i in range(len(benefit_options))])[0]
        benefit_type = benefit_types[selected_index]

        # Calculate benefit amount (between 10% and 47% of the cost based on type)
        # RIs typically save 20-45%, Savings Plans 15-30%, AHB up to 47%
        if "Reserved Instance: 3 year" in benefit_type["full_name"]:
            benefit_percent = random.uniform(0.30, 0.45)
        elif "Reserved Instance: 1 year" in benefit_type["full_name"]:
            benefit_percent = random.uniform(0.20, 0.35)
        elif "Savings Plan" in benefit_type["full_name"]:
            benefit_percent = random.uniform(0.15, 0.30)
        elif "Hybrid Benefit" in benefit_type["full_name"]:
            benefit_percent = random.uniform(0.30, 0.47)
        else:
            benefit_percent = random.uniform(0.10, 0.25)

        benefit_amount = -1 * cost * benefit_percent  # Benefits are negative

        benefit = {
            "name": benefit_type["name"],
            "full_name": benefit_type["full_name"],
            "type": benefit_type["id"],
            "id": benefit_type["id"],
            "term": benefit_type["term"],
            "order_id": benefit_type["order_id"],
            "order_name": benefit_type["order_name"],
            "amount": benefit_amount
        }

        benefits.append(benefit)

    return benefits


def generate_usage_data(project_name, project_data, day_count, start_date, daily_budget):
    """
    Generate usage data for a specific project following Azure Cost Management format.
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
    regions = CONFIG["azure_regions"]
    if not regions:
        regions = ["eastus", "westus"]  # Default if no regions defined

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

                # Get subscription details
                subscription_details = get_subscription_details(stage_name)
                subscription_id = subscription_details["subscription_id"]
                subscription_name = subscription_details["subscription_name"]

                # Get billing account for this subscription
                billing_account_id = get_billing_account_for_subscription(
                    subscription_name)

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
                            service_family = category  # Store service family for later
                            break

                    if not service_details:
                        continue

                    # Service description and category mapping
                    meter_category = service_name
                    meter_subcategory = "Standard"
                    consumed_service = f"Microsoft.{service_family}"

                    # Create or reuse resource names
                    if service_name not in resource_names or region not in resource_names[service_name]:
                        resource_names[service_name][region] = []

                        # Generate resources based on settings
                        num_resources = DATA_VOLUME_SETTINGS["max_resources_per_service"]
                        for _ in range(num_resources):
                            vm_size = None
                            if service_name == "VirtualMachines" and "vm_sizes" in service_details and service_details["vm_sizes"]:
                                vm_size = random.choice(
                                    service_details["vm_sizes"])

                            # Get resource name
                            resource_name = generate_resource_name(
                                service_name, project_name, region, vm_size)

                            # Generate resource group name
                            resource_group_name = f"{resource_name.split('-')[0]}-rg"

                            # Create Azure resource ID
                            resource_id = generate_resource_id(
                                subscription_id,
                                resource_name,
                                service_name,
                                resource_group_name
                            )

                            resource_names[service_name][region].append({
                                "name": resource_name,
                                "id": resource_id,
                                "vm_size": vm_size,
                                "resource_group": resource_group_name,
                                "subscription_id": subscription_id,
                                "subscription_name": subscription_name
                            })

                            # Generate tags for this resource
                            resource_tags = generate_tags(
                                service_name,
                                resource_name,
                                project_name,
                                project_data,
                                stage_name,
                                vm_size
                            )

                            # Store tags for later reference
                            for key, value in resource_tags.items():
                                tags_data.append({
                                    "resource_id": resource_id,
                                    "key": key,
                                    "value": value
                                })

                    # Distribute budget across resources
                    num_resources = len(resource_names[service_name][region])
                    resource_budget = region_budget / num_resources if num_resources > 0 else 0

                    for resource_data in resource_names[service_name][region]:
                        resource_name = resource_data["name"]
                        resource_id = resource_data["id"]
                        vm_size = resource_data["vm_size"]
                        resource_group = resource_data["resource_group"]

                        if resource_budget <= 0:
                            continue

                        # Generate usage records based on settings
                        num_usage_records = random.randint(
                            1, DATA_VOLUME_SETTINGS["max_usage_records_per_day"])

                        for _ in range(num_usage_records):
                            # Determine charge type (Usage, Purchase, Adjustment, Tax)
                            charge_type = random.choices(
                                ["Usage", "Tax", "Adjustment", "Usage"],
                                weights=[0.90, 0.07, 0.02, 0.01])[0]

                            # Determine usage amount, rate, and cost
                            base_rate = service_details.get("base_rate", 0.01)

                            # Apply some randomness to the rate
                            rate_variability = random.uniform(0.9, 1.1)
                            rate = base_rate * rate_variability

                            # Get unit for this service
                            unit_of_measure = service_details.get(
                                "unit", "Hour")

                            # Calculate effective price (after discounts)
                            effective_price = calculate_effective_price(
                                service_name, subscription_id, rate)

                            # Calculate usage amount based on budget and effective price
                            quantity = resource_budget / effective_price / \
                                num_usage_records if effective_price > 0 else 0

                            # Calculate cost
                            cost = quantity * effective_price

                            # For special charge types
                            if charge_type == "Tax":
                                # Tax is typically a percentage of the cost
                                quantity = 1.0
                                tax_rate = resource_budget * 0.1 / num_usage_records  # 10% tax
                                cost = tax_rate
                                effective_price = tax_rate

                            elif charge_type == "Adjustment":
                                # Adjustments can be credits or additional charges
                                adjustment_sign = 1 if random.random() < 0.3 else -1  # 70% are credits (negative)
                                adjustment_percent = random.uniform(
                                    0.05, 0.2)  # 5-20% adjustment
                                cost = adjustment_sign * resource_budget * \
                                    adjustment_percent / num_usage_records
                                quantity = 1.0
                                effective_price = cost  # For adjustments, price equals cost

                            # Choose a random operation and meter from service details
                            operations = service_details.get(
                                "operations", ["Standard"])
                            operation = random.choice(operations)

                            # Meter ID and description
                            meter_ids = service_details.get(
                                "meter_ids", ["00000000-0000-0000-0000-000000000000"])
                            meter_id = random.choice(meter_ids)

                            # Generate meter name using pattern
                            meter_name_pattern = service_details.get(
                                "meter_name_pattern", "{service} {operation} in {region}")
                            meter_name = meter_name_pattern.format(
                                service=service_name,
                                operation=operation,
                                region=region
                            )

                            # Format date in ISO format - Azure uses YYYY-MM-DD
                            date_str = current_date.strftime('%Y-%m-%d')

                            # Billing period details
                            month_start = datetime.date(
                                current_date.year, current_date.month, 1)
                            next_month = month_start.month + 1 if month_start.month < 12 else 1
                            next_month_year = month_start.year if month_start.month < 12 else month_start.year + 1
                            month_end = datetime.date(
                                next_month_year, next_month, 1) - datetime.timedelta(days=1)

                            billing_period_start = month_start.strftime(
                                '%Y-%m-%d')
                            billing_period_end = month_end.strftime('%Y-%m-%d')

                            # Generate additional info
                            additional_info = json.dumps({
                                "serviceInfo": f"{service_name} {operation}",
                                "resourceDetails": {
                                    "resourceName": resource_name,
                                    "region": region,
                                    "resourceType": get_resource_type_path(service_name),
                                },
                                "metricDetails": {
                                    "meterName": meter_name,
                                    "meterCategory": meter_category,
                                    "unit": unit_of_measure,
                                }
                            })

                            # Generate resource tags in JSON format
                            tags_json = {}
                            for tag_record in tags_data:
                                if tag_record["resource_id"] == resource_id:
                                    tags_json[tag_record["key"]
                                              ] = tag_record["value"]

                            # Serialize tags to JSON string
                            tags_str = json.dumps(tags_json)

                            # Generate benefit information
                            benefit_info = generate_benefits(
                                service_name, cost, subscription_id)

                            # Get Azure offer ID
                            offer_id = get_azure_offer_id(
                                subscription_id, subscription_name)

                            # Generate cost allocation rule name if applicable
                            cost_allocation_rule = generate_cost_allocation_rule(
                                resource_id, tags_data)

                            # Populate benefit fields if applicable
                            benefit_id = ""
                            benefit_name = ""
                            term = ""
                            product_order_id = ""
                            product_order_name = ""
                            if benefit_info:
                                benefit_id = benefit_info[0]["id"]
                                benefit_name = benefit_info[0]["full_name"]
                                term = benefit_info[0].get("term", "")
                                product_order_id = benefit_info[0].get(
                                    "order_id", "")
                                product_order_name = benefit_info[0].get(
                                    "order_name", "")

                            # Determine pricing model
                            pricing_model = service_details.get(
                                "pricing_model", "on_demand")
                            if "Reserved" in benefit_name:
                                pricing_model = "reservation"
                            elif "Savings" in benefit_name:
                                pricing_model = "savings_plan"

                            # Determine service tier
                            service_tier = "Standard"
                            if "Premium" in operation:
                                service_tier = "Premium"
                            elif "Basic" in operation:
                                service_tier = "Basic"

                            # Create the record using Azure Cost Management schema
                            record = {
                                "BillingAccountId": billing_account_id,
                                "BillingAccountName": f"Billing Account {billing_account_id[:8]}",
                                "BillingPeriodStartDate": billing_period_start,
                                "BillingPeriodEndDate": billing_period_end,
                                "BillingProfileId": f"billing-profile-{billing_account_id[:8]}",
                                "BillingProfileName": "Enterprise Agreement",
                                "AccountOwnerId": f"owner-{subscription_id[-8:]}",
                                "AccountName": project_business_unit,
                                "SubscriptionId": subscription_id,
                                "SubscriptionName": subscription_name,
                                "Date": date_str,
                                "Product": service_name,
                                "PartNumber": f"Part-{meter_id[-6:]}",
                                "MeterId": meter_id,
                                "ServiceFamily": service_family,
                                "MeterCategory": meter_category,
                                "MeterSubCategory": meter_subcategory,
                                "MeterName": meter_name,
                                "MeterRegion": region,
                                "UnitOfMeasure": unit_of_measure,
                                "Quantity": quantity,
                                "EffectivePrice": effective_price,
                                "Cost": cost,
                                "CostInBillingCurrency": cost,
                                "CostCenter": tags_json.get("cost-center", f"{project_business_unit}-CC{random.randint(1000, 9999)}"),
                                "ResourceLocation": region,
                                "ConsumedService": consumed_service,
                                "ResourceId": resource_id,
                                "ResourceName": resource_name,
                                "ServiceName": service_name,
                                "ServiceTier": service_tier,
                                "ResourceGroupName": resource_group,
                                "ResourceType": get_resource_type_path(service_name),
                                "PublisherType": "Microsoft",
                                "PublisherName": "Microsoft",
                                "ReservationId": benefit_id if "Reserved Instance" in benefit_name else "",
                                "ReservationName": benefit_name if "Reserved Instance" in benefit_name else "",
                                "ProductOrderId": product_order_id,
                                "ProductOrderName": product_order_name,
                                "OfferId": offer_id,
                                "BenefitId": benefit_id,
                                "BenefitName": benefit_name,
                                "Term": term,
                                "CostAllocationRuleName": cost_allocation_rule,
                                "Tags": tags_str,
                                "AdditionalInfo": additional_info,
                                "ServiceInfo1": f"{service_name} {operation}",
                                "ServiceInfo2": meter_name,
                                "PricingModel": pricing_model,
                                "ChargeType": charge_type,
                                "Frequency": "Recurring",
                                "PricingCurrency": "USD"
                            }

                            results.append(record)

                            # Subtract from budget for subsequent calculations
                            resource_budget -= cost

    return results, tags_data


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
    Find services that are referenced in projects but not defined in AZURE_SERVICES.
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
                "unit": "Hour",
                "usage_types": [f"{service}-Usage"],
                "meter_name_pattern": f"{service} {{operation}} in {{region}}",
                "meter_ids": [f"{uuid.uuid4().hex[:12].upper()}"]
            }

    return missing


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

    # First, merge the tags data with the billing data
    # Extract resource IDs
    df_records['resource_id'] = df_records['ResourceId']

    # Create a mapping of resources to chargeback entities
    resource_to_entity = {}
    resource_allocation_method = {}

    for _, tag in df_tags.iterrows():
        if tag['key'] == 'chargeback-entity':
            resource_to_entity[tag['resource_id']] = tag['value']
        if tag['key'] == 'allocation-method':
            resource_allocation_method[tag['resource_id']] = tag['value']

    # Apply mapping to get chargeback entity for each record
    df_records['chargeback_entity'] = df_records['resource_id'].map(
        resource_to_entity).fillna("Unallocated")

    df_records['allocation_method'] = df_records['resource_id'].map(
        resource_allocation_method).fillna("direct")

    # Convert invoice date to a simpler format
    df_records['month'] = pd.to_datetime(
        df_records['Date']).dt.strftime('%Y-%m')

    # 1. Direct Chargeback Report - what each entity should be charged
    chargeback_summary = df_records.groupby(['month', 'chargeback_entity'])[
        'Cost'].sum().reset_index()
    chargeback_summary.to_csv(
        f"{output_dir}/chargeback_by_entity.csv", index=False)

    # 2. Generate by Service and Entity
    service_entity_summary = df_records.groupby(
        ['month', 'chargeback_entity', 'ServiceName'])['Cost'].sum().reset_index()
    service_entity_summary.to_csv(
        f"{output_dir}/chargeback_by_service_entity.csv", index=False)

    # 3. Credit Impact Analysis
    # Extract benefits from the BenefitName column
    total_costs = df_records['Cost'].sum()

    # 4. Allocation Methods Report
    allocation_summary = df_records.groupby(['month', 'allocation_method'])[
        'Cost'].sum().reset_index()
    allocation_summary.to_csv(
        f"{output_dir}/cost_by_allocation_method.csv", index=False)

    return {
        'chargeback_total': chargeback_summary['Cost'].sum(),
        'direct_allocation': allocation_summary[allocation_summary['allocation_method'] == 'direct']['Cost'].sum(),
        'shared_allocation': allocation_summary[allocation_summary['allocation_method'] != 'direct']['Cost'].sum(),
    }


def analyze_discount_impact(df_records, output_dir):
    """Analyze the impact of discounts and benefits on costs"""

    # Extract benefit information
    benefit_records = df_records[df_records['BenefitName'] != ""]
    no_benefit_records = df_records[df_records['BenefitName'] == ""]

    # Calculate effective costs with and without benefits
    total_cost = df_records['Cost'].sum()
    cost_with_benefits = benefit_records['Cost'].sum()
    cost_without_benefits = no_benefit_records['Cost'].sum()

    # Estimate benefit amount - this is an approximation as the raw benefit amount is not directly available
    # In a real Azure Cost Management export, this would be based on the amortized cost difference
    estimated_benefit_amount = cost_with_benefits * - \
        0.25  # Assuming 25% average discount

    # Calculate effective cost after benefits
    effective_cost = total_cost + estimated_benefit_amount

    # Summary by subscription
    subscription_summary = df_records.groupby(['SubscriptionId', 'SubscriptionName'])[
        ['Cost']].sum().reset_index()

    # Add benefit info per subscription
    benefit_by_sub = benefit_records.groupby(
        ['SubscriptionId'])[['Cost']].sum()
    no_benefit_by_sub = no_benefit_records.groupby(['SubscriptionId'])[
        ['Cost']].sum()

    # Merge into subscription summary
    subscription_summary = subscription_summary.set_index('SubscriptionId')
    subscription_summary['BenefitCost'] = benefit_by_sub['Cost'] if not benefit_by_sub.empty else 0
    subscription_summary['NonBenefitCost'] = no_benefit_by_sub['Cost'] if not no_benefit_by_sub.empty else 0
    # Assuming 25% savings
    subscription_summary['EstimatedSavings'] = subscription_summary['BenefitCost'] * 0.25
    subscription_summary['BenefitPercentage'] = (subscription_summary['EstimatedSavings'] /
                                                 subscription_summary['Cost'] * 100).fillna(0)
    subscription_summary = subscription_summary.reset_index()

    subscription_summary.to_csv(
        f"{output_dir}/benefit_impact_by_subscription.csv", index=False)

    # Summary by service
    service_summary = df_records.groupby(['ServiceName'])[
        ['Cost']].sum().reset_index()

    # Add benefit info per service
    benefit_by_service = benefit_records.groupby(['ServiceName'])[
        ['Cost']].sum()
    no_benefit_by_service = no_benefit_records.groupby(['ServiceName'])[
        ['Cost']].sum()

    # Merge into service summary
    service_summary = service_summary.set_index('ServiceName')
    service_summary['BenefitCost'] = benefit_by_service['Cost'] if not benefit_by_service.empty else 0
    service_summary['NonBenefitCost'] = no_benefit_by_service['Cost'] if not no_benefit_by_service.empty else 0
    # Assuming 25% savings
    service_summary['EstimatedSavings'] = service_summary['BenefitCost'] * 0.25
    service_summary['BenefitPercentage'] = (service_summary['EstimatedSavings'] /
                                            service_summary['Cost'] * 100).fillna(0)
    service_summary = service_summary.reset_index()

    service_summary.to_csv(
        f"{output_dir}/benefit_impact_by_service.csv", index=False)

    # Find resources with the largest benefit amounts
    # Group by resource and sum costs
    resource_summary = df_records.groupby(['ResourceId', 'ResourceName', 'BenefitName'])[
        ['Cost']].sum().reset_index()

    # Keep only records with benefits
    resource_summary_with_benefits = resource_summary[resource_summary['BenefitName'] != ""]

    # Calculate estimated savings
    resource_summary_with_benefits['EstimatedSavings'] = resource_summary_with_benefits['Cost'] * 0.25

    # Sort by estimated savings (largest savings first)
    resource_summary_with_benefits = resource_summary_with_benefits.sort_values(
        'EstimatedSavings', ascending=False)

    top_resources = resource_summary_with_benefits.head(20)
    top_resources.to_csv(
        f"{output_dir}/top_benefit_impact_resources.csv", index=False)

    # Overall statistics
    summary_stats = {
        'total_cost': total_cost,
        'cost_with_benefits': cost_with_benefits,
        'cost_without_benefits': cost_without_benefits,
        'estimated_benefit_amount': estimated_benefit_amount,
        'effective_cost': effective_cost,
        'percent_discount': (estimated_benefit_amount / total_cost * 100) if total_cost > 0 else 0,
        'subscriptions_with_benefits': len(subscription_summary[subscription_summary['EstimatedSavings'] > 0]),
    }

    # Save summary stats
    with open(f"{output_dir}/benefit_impact_summary.json", 'w') as f:
        json.dump(summary_stats, f, indent=2)

    return summary_stats


def main():
    print("Azure Cost Management Data Generator")
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
            f"WARNING: Found services in projects that are not defined in AZURE_SERVICES: {', '.join(missing_services)}")

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
    for col in COST_MANAGEMENT_COLUMNS:
        if col not in df_records.columns:
            df_records[col] = ""

    for col in RESOURCE_TAGS_COLUMNS:
        if col not in df_tags.columns:
            df_tags[col] = ""

    # Save to CSV
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    df_records.to_csv(
        f"{output_dir}/azure_cost_management_export.csv", index=False)
    df_tags.to_csv(f"{output_dir}/resource_tags.csv", index=False)

    # Save the project lifecycle mapping
    project_lifecycle_df.to_csv(
        f"{output_dir}/project_lifecycle_mapping.csv", index=False)
    print(
        f"Saved project lifecycle mapping to {output_dir}/project_lifecycle_mapping.csv")

    # Generate a summary per subscription per month
    if not df_records.empty:
        # Extract month from Date column
        df_records['month'] = pd.to_datetime(
            df_records['Date']).dt.strftime('%Y-%m')

        # Create subscription summary
        subscription_summary = df_records.groupby(['month', 'SubscriptionName'])[
            'Cost'].sum().reset_index()
        subscription_summary.to_csv(
            f"{output_dir}/cost_summary_by_subscription.csv", index=False)

        # Generate summary by service
        service_summary = df_records.groupby(['month', 'ServiceName'])[
            'Cost'].sum().reset_index()
        service_summary.to_csv(
            f"{output_dir}/cost_summary_by_service.csv", index=False)

        # Map project names to business units using tags
        # First create a mapping from ResourceId to business unit
        resource_to_bu = {}
        for _, tag in df_tags.iterrows():
            if tag['key'] == 'business-unit':
                resource_to_bu[tag['resource_id']] = tag['value']

        # Apply mapping to get business unit
        df_records['business_unit'] = df_records['ResourceId'].map(
            resource_to_bu).fillna("Unknown")

        # Generate monthly cost summary by business unit
        bu_summary = df_records.groupby(['month', 'business_unit'])[
            'Cost'].sum().reset_index()
        bu_summary.to_csv(
            f"{output_dir}/cost_summary_by_business_unit.csv", index=False)

        # Generate chargeback/showback reports
        chargeback_stats = generate_chargeback_reports(
            df_records, df_tags, output_dir)
        print(
            f"Generated chargeback/showback reports. Total chargeback: ${chargeback_stats['chargeback_total']:.2f}")

        # Analyze benefit impact
        benefit_impact = analyze_discount_impact(df_records, output_dir)
        print(f"Analyzed benefit impact. Estimated savings: ${benefit_impact['estimated_benefit_amount']:.2f} " +
              f"({benefit_impact['percent_discount']:.2f}%)")

    end_time = time.time()
    print(
        f"Generated Azure Cost Management data in {end_time - start_time:.2f} seconds")
    print(f"Data saved to {output_dir}/")


if __name__ == "__main__":
    main()
