#!/usr/bin/env python3
"""
Multi-Cloud Cost and Usage Data Generator

This module coordinates billing data generation across AWS, GCP, and Azure
to simulate realistic multi-cloud deployment scenarios.
"""

import os
import json
import datetime
import pandas as pd
import numpy as np
import random
import multiprocessing
import time
import uuid
from collections import defaultdict

# Import single-cloud generators
import aws_cur_data_generator
from aws_config import CONFIG as AWS_CONFIG
import GCP_billing_data_generator
from configGCP import CONFIG as GCP_CONFIG
import Azure_billing_data_generator
from configAzure import CONFIG as AZURE_CONFIG

# Import multi-cloud configurations
try:
    from config_multi_cloud import MULTI_CLOUD_PROJECTS
except ImportError:
    # Default if multi-cloud config not available yet
    MULTI_CLOUD_PROJECTS = {}

# Constants and settings
OUTPUT_DIR = "output/multi-cloud"
CURRENCY = "USD"
CLOUD_PLATFORMS = ["aws", "azure", "gcp"]

# Multi-cloud lifecycle patterns
MULTI_CLOUD_PATTERNS = {
    "steady_state": {
        "description": "Stable distribution across multiple clouds",
        "handler": "handle_steady_state"
    },
    "migration": {
        "description": "Gradual transition from one cloud to another",
        "handler": "handle_migration"
    },
    "expansion": {
        "description": "Adding a new cloud platform over time",
        "handler": "handle_expansion"
    },
    "consolidation": {
        "description": "Reducing the number of cloud platforms over time",
        "handler": "handle_consolidation"
    },
    "dr_scenario": {
        "description": "Primary and DR cloud with periodic DR testing",
        "handler": "handle_dr_scenario"
    },
    "burst_scaling": {
        "description": "Using secondary cloud for overflow capacity",
        "handler": "handle_burst_scaling"
    },
    "cloud_repatriation": {
        "description": "Moving workloads back from public cloud to on-premises",
        "handler": "handle_repatriation"
    }
}

# Data volume settings - control amount of data generated
DATA_VOLUME_SETTINGS = {
    "days_to_generate": 11,           # Number of days to generate data for
    "sampling_interval": 5,            # Generate data every X days
    "on_prem_cost_simulation": True,   # Generate simulated on-premises costs
    "volatility_factor": 0.02,         # Cost volatility factor
    "max_projects": 1,                # Maximum number of projects to process
}


def create_output_directories():
    """Create necessary output directories."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for platform in CLOUD_PLATFORMS:
        os.makedirs(f"{OUTPUT_DIR}/{platform}", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/consolidated", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/visualizations", exist_ok=True)


def calculate_annual_budget():
    """Calculate total annual budget across all platforms."""
    # Sum of budgets from individual platforms
    aws_budget = AWS_CONFIG.get("annual_budget", 50000000)
    gcp_budget = GCP_CONFIG.get("annual_budget", 50000000)
    azure_budget = AZURE_CONFIG.get("annual_budget", 50000000)

    # Default to 150M if configs are missing budgets
    return aws_budget + gcp_budget + azure_budget


def apply_multi_cloud_lifecycle(base_lifecycle, day_index, total_days, pattern_type, pattern_params, cloud):
    """
    Applies multi-cloud specific lifecycle adjustments.

    Args:
        base_lifecycle: The base lifecycle pattern from single-cloud config
        day_index: Current day index
        total_days: Total number of days
        pattern_type: Type of multi-cloud pattern
        pattern_params: Parameters for the pattern
        cloud: Current cloud platform

    Returns:
        Adjustment factor to apply to usage
    """
    if pattern_type == "steady_state":
        # No adjustment needed for steady state - use base lifecycle
        return 1.0

    elif pattern_type == "migration":
        source_cloud = pattern_params.get("source_cloud")
        target_cloud = pattern_params.get("target_cloud")
        migration_start_day = int(
            total_days * pattern_params.get("start_ratio", 0.3))
        migration_duration = int(
            total_days * pattern_params.get("duration_ratio", 0.3))
        migration_end_day = migration_start_day + migration_duration

        if day_index < migration_start_day:
            # Before migration starts
            if cloud == source_cloud:
                return 1.0  # Full usage on source cloud
            elif cloud == target_cloud:
                return 0.1  # Minimal usage on target (planning/setup)
            else:
                return 1.0  # Other clouds unaffected

        elif day_index >= migration_start_day and day_index <= migration_end_day:
            # During migration - linear transition
            progress = (day_index - migration_start_day) / migration_duration
            if cloud == source_cloud:
                return 1.0 - (progress * 0.9)  # Gradual reduction to 10%
            elif cloud == target_cloud:
                return 0.1 + (progress * 0.9)  # Gradual increase to 100%
            else:
                return 1.0  # Other clouds unaffected

        else:
            # After migration
            if cloud == source_cloud:
                return 0.1  # Minimal remaining usage on source
            elif cloud == target_cloud:
                return 1.0  # Full usage on target
            else:
                return 1.0  # Other clouds unaffected

    elif pattern_type == "expansion":
        new_cloud = pattern_params.get("new_cloud")
        expansion_start_day = int(
            total_days * pattern_params.get("start_ratio", 0.3))
        expansion_duration = int(
            total_days * pattern_params.get("duration_ratio", 0.3))
        expansion_end_day = expansion_start_day + expansion_duration

        if cloud == new_cloud:
            if day_index < expansion_start_day:
                return 0.1  # Minimal initial usage
            elif day_index >= expansion_start_day and day_index <= expansion_end_day:
                progress = (day_index - expansion_start_day) / \
                    expansion_duration
                return 0.1 + (progress * 0.9)  # Gradual increase
            else:
                return 1.0  # Full usage after expansion
        else:
            return 1.0  # Other clouds maintain normal patterns

    elif pattern_type == "consolidation":
        removed_cloud = pattern_params.get("removed_cloud")
        consolidation_start_day = int(
            total_days * pattern_params.get("start_ratio", 0.3))
        consolidation_duration = int(
            total_days * pattern_params.get("duration_ratio", 0.3))
        consolidation_end_day = consolidation_start_day + consolidation_duration
        target_cloud = pattern_params.get("target_cloud")

        if cloud == removed_cloud:
            if day_index < consolidation_start_day:
                return 1.0  # Full usage before consolidation
            elif day_index >= consolidation_start_day and day_index <= consolidation_end_day:
                progress = (day_index - consolidation_start_day) / \
                    consolidation_duration
                return 1.0 - (progress * 0.9)  # Gradual reduction
            else:
                return 0.1  # Minimal remaining usage after consolidation
        elif cloud == target_cloud:
            # Target cloud gets a boost as workloads consolidate to it
            if day_index < consolidation_start_day:
                return 1.0  # Normal usage before consolidation
            elif day_index >= consolidation_start_day and day_index <= consolidation_end_day:
                progress = (day_index - consolidation_start_day) / \
                    consolidation_duration
                # Growth factor depends on relative sizes of workloads
                transferred_workload = pattern_params.get(
                    "workload_ratio", 0.5)
                # Gradual increase
                return 1.0 + (progress * transferred_workload)
            else:
                # Sustained higher usage
                return 1.0 + pattern_params.get("workload_ratio", 0.5)
        else:
            return 1.0  # Other clouds unaffected

    elif pattern_type == "dr_scenario":
        primary_cloud = pattern_params.get("primary_cloud")
        dr_cloud = pattern_params.get("dr_cloud")

        # Simulate periodic DR tests and possibly a failover event
        dr_test_frequency = pattern_params.get("test_frequency_days", 90)
        dr_test_duration = pattern_params.get("test_duration_days", 3)
        failover_day = pattern_params.get("failover_day", None)
        failover_duration = pattern_params.get("failover_duration_days", 7)

        # Check if today is a DR test day
        is_dr_test = (day_index % dr_test_frequency < dr_test_duration)

        # Check if today is during failover
        is_failover = False
        if failover_day is not None:
            is_failover = (day_index >= failover_day and day_index <
                           failover_day + failover_duration)

        if cloud == primary_cloud:
            if is_failover:
                return 0.1  # Primary cloud mostly down during failover
            else:
                return 1.0  # Normal operation
        elif cloud == dr_cloud:
            if is_failover:
                return 2.0  # DR cloud handling all traffic during failover
            elif is_dr_test:
                return 0.5  # Elevated usage during DR test
            else:
                return 0.1  # Minimal standby usage
        else:
            return 1.0  # Other clouds unaffected

    elif pattern_type == "burst_scaling":
        primary_cloud = pattern_params.get("primary_cloud")
        burst_cloud = pattern_params.get("burst_cloud")
        burst_threshold = pattern_params.get("threshold", 0.8)
        burst_frequency = pattern_params.get("frequency_days", 30)
        burst_duration = pattern_params.get("duration_days", 5)

        # Determine if today is in a burst period
        is_burst_period = (day_index % burst_frequency < burst_duration)

        if cloud == primary_cloud:
            if is_burst_period:
                return burst_threshold  # Primary cloud at capacity
            else:
                return 0.7  # Normal operation below threshold
        elif cloud == burst_cloud:
            if is_burst_period:
                # Calculate overflow amount
                overflow_factor = pattern_params.get("overflow_factor", 0.6)
                return overflow_factor  # Significant usage during burst
            else:
                return 0.1  # Minimal standby usage
        else:
            return 1.0  # Other clouds unaffected

    elif pattern_type == "cloud_repatriation":
        cloud_source = pattern_params.get("cloud_source")
        repatriation_start_day = int(
            total_days * pattern_params.get("start_ratio", 0.3))
        repatriation_duration = int(
            total_days * pattern_params.get("duration_ratio", 0.4))
        repatriation_end_day = repatriation_start_day + repatriation_duration

        if cloud == cloud_source:
            if day_index < repatriation_start_day:
                return 1.0  # Full cloud usage before repatriation
            elif day_index >= repatriation_start_day and day_index <= repatriation_end_day:
                progress = (day_index - repatriation_start_day) / \
                    repatriation_duration
                # Gradual reduction (30% remains in cloud)
                return 1.0 - (progress * 0.7)
            else:
                return 0.3  # Reduced long-term cloud footprint
        else:
            return 1.0  # Other clouds unaffected

    # Default - no adjustment
    return 1.0


def generate_cloud_distribution_factors(multi_cloud_project, day_index, total_days):
    """
    Generate distribution factors for each cloud platform based on multi-cloud pattern.

    Args:
        multi_cloud_project: Project configuration
        day_index: Current day index
        total_days: Total number of days

    Returns:
        Dictionary of distribution factors for each cloud
    """
    pattern_type = multi_cloud_project["multi_cloud_pattern"]["type"]
    pattern_params = multi_cloud_project["multi_cloud_pattern"].get(
        "params", {})

    # Start with base percentages from configuration
    distribution = {}
    for cloud, cloud_config in multi_cloud_project["clouds"].items():
        distribution[cloud] = cloud_config.get("percentage", 0)

    # Apply lifecycle adjustments based on pattern type
    for cloud in distribution:
        base_lifecycle = multi_cloud_project["clouds"][cloud].get(
            "base_lifecycle", "steady_state")
        adjustment = apply_multi_cloud_lifecycle(
            base_lifecycle, day_index, total_days, pattern_type, pattern_params, cloud
        )
        distribution[cloud] *= adjustment

    # Normalize to ensure percentages sum to 1.0
    total = sum(distribution.values())
    if total > 0:
        for cloud in distribution:
            distribution[cloud] /= total

    return distribution


def prepare_single_cloud_data(cloud, project_name, project_config, annual_budget, start_date, end_date):
    """
    Prepare project data for a single cloud platform.

    Args:
        cloud: Cloud platform identifier (aws, gcp, azure)
        project_name: Name of the multi-cloud project
        project_config: Cloud-specific project configuration
        annual_budget: Total annual budget
        start_date: Start date for generation
        end_date: End date for generation

    Returns:
        Processed and formatted project data for the specified cloud
    """
    # Extract cloud-specific configuration
    cloud_config = project_config["clouds"].get(cloud, {})
    if not cloud_config:
        return None, None

    # Get services and stages for this cloud
    services = cloud_config.get("services", [])
    stages = cloud_config.get("stages", [])

    if not services or not stages:
        return None, None

    # Create a compatible project configuration for the cloud-specific generator
    adjusted_project = {
        "description": project_config.get("description", ""),
        "use_case": project_config.get("use_case", "Enterprise Applications"),
        "lifecycle": cloud_config.get("base_lifecycle", "steady_state"),
        "services": services,
        "stages": stages,
        "business_unit": project_config.get("business_unit", "IT"),
        # Add multi-cloud metadata to track the relationship
        "multi_cloud_project": project_name,
        "cloud_percentage": cloud_config.get("percentage", 0),
    }

    # Determine cloud-specific configurations and generators
    if cloud == "aws":
        config = AWS_CONFIG
        generator = aws_cur_data_generator
    elif cloud == "gcp":
        config = GCP_CONFIG
        generator = GCP_billing_data_generator
    elif cloud == "azure":
        config = AZURE_CONFIG
        generator = Azure_billing_data_generator
    else:
        return None, None

    # Calculate cloud and project budgets
    cloud_percentage = cloud_config.get("percentage", 0)
    cloud_budget = annual_budget * cloud_percentage

    return adjusted_project, (generator, config, cloud_budget)


def process_multi_cloud_project(args):
    """
    Process a single multi-cloud project - for parallel execution.

    Args:
        args: Tuple containing project and generation parameters

    Returns:
        Dictionary of results for each cloud platform
    """
    project_name, project_config, start_date, end_date, annual_budget = args

    try:
        print(f"Processing multi-cloud project: {project_name}")
        project_results = {}

        day_count = (end_date - start_date).days

        # Process each cloud platform
        for cloud in CLOUD_PLATFORMS:
            if cloud not in project_config["clouds"]:
                continue

            # Prepare project data for this cloud
            adjusted_project, generator_info = prepare_single_cloud_data(
                cloud, project_name, project_config, annual_budget, start_date, end_date
            )

            if not adjusted_project or not generator_info:
                continue

            generator, config, cloud_budget = generator_info

            # Calculate daily budget
            daily_budget = cloud_budget / 365.0

            # Get cloud-specific generation function
            if cloud == "aws":
                results, tags = generator.generate_usage_data(
                    project_name, adjusted_project, day_count, start_date, daily_budget
                )
            elif cloud == "gcp":
                results, tags = generator.generate_usage_data(
                    project_name, adjusted_project, day_count, start_date, daily_budget
                )
            elif cloud == "azure":
                results, tags = generator.generate_usage_data(
                    project_name, adjusted_project, day_count, start_date, daily_budget
                )

            # Store results
            project_results[cloud] = {
                "billing_data": results,
                "tag_data": tags
            }

            print(
                f"  Generated {len(results)} records for {cloud} in project {project_name}")

        return project_name, project_results

    except Exception as e:
        import traceback
        print(f"Error processing project {project_name}: {e}")
        print(traceback.format_exc())
        return project_name, {}


def apply_day_specific_adjustments(billing_data, cloud, project_name, project_config, day_index, total_days):
    """
    Apply day-specific adjustments to billing data based on multi-cloud pattern.

    Args:
        billing_data: List of billing data records
        cloud: Cloud platform identifier
        project_name: Name of the multi-cloud project
        project_config: Project configuration
        day_index: Current day index
        total_days: Total number of days

    Returns:
        Adjusted billing data
    """
    pattern_type = project_config["multi_cloud_pattern"]["type"]
    pattern_params = project_config["multi_cloud_pattern"].get("params", {})

    # Apply adjustments based on pattern type
    for record in billing_data:
        # Get date from record (format varies by cloud)
        record_date = None
        if cloud == "aws":
            if "lineItem/UsageStartDate" in record:
                record_date = datetime.datetime.strptime(
                    record["lineItem/UsageStartDate"].split("T")[0], "%Y-%m-%d"
                ).date()
        elif cloud == "gcp":
            if "usage_start_time" in record:
                record_date = datetime.datetime.strptime(
                    record["usage_start_time"].split("T")[0], "%Y-%m-%d"
                ).date()
        elif cloud == "azure":
            if "Date" in record:
                record_date = datetime.datetime.strptime(
                    record["Date"], "%Y-%m-%d"
                ).date()

        if not record_date:
            continue

        # Calculate day index for this record
        record_day_index = (record_date - start_date).days

        # Skip if not matching our current day
        if record_day_index != day_index:
            continue

        # Apply multi-cloud lifecycle adjustment
        base_lifecycle = project_config["clouds"][cloud].get(
            "base_lifecycle", "steady_state")
        adjustment = apply_multi_cloud_lifecycle(
            base_lifecycle, day_index, total_days, pattern_type, pattern_params, cloud
        )

        # Apply cost adjustments
        if cloud == "aws":
            record["lineItem/UnblendedCost"] *= adjustment
            record["lineItem/BlendedCost"] *= adjustment
        elif cloud == "gcp":
            record["cost"] *= adjustment
        elif cloud == "azure":
            record["Cost"] *= adjustment

    return billing_data


def normalize_cloud_schema(record, cloud, multi_cloud_project):
    """
    Normalize billing data schema across different cloud platforms.

    Args:
        record: Original billing record
        cloud: Cloud platform identifier
        multi_cloud_project: Name of the multi-cloud project

    Returns:
        Normalized record with common schema
    """
    normalized = {
        "cloud": cloud,
        "multi_cloud_project": multi_cloud_project,
        "date": None,
        "service": None,
        "resource_id": None,
        "cost": 0.0,
        "account_id": None,
        "region": None,
        "usage_quantity": 0.0,
        "usage_unit": None,
    }

    # Extract fields based on cloud platform
    if cloud == "aws":
        normalized["date"] = record.get("lineItem/UsageStartDate", "").split("T")[
            0] if "lineItem/UsageStartDate" in record else ""
        normalized["service"] = record.get("lineItem/ProductCode", "")
        normalized["resource_id"] = record.get("lineItem/ResourceId", "")
        normalized["cost"] = float(record.get("lineItem/UnblendedCost", 0.0))
        normalized["account_id"] = record.get("lineItem/UsageAccountId", "")
        normalized["region"] = record.get("product/region", "")
        normalized["usage_quantity"] = float(
            record.get("lineItem/UsageAmount", 0.0))
        normalized["usage_unit"] = record.get("pricing/unit", "")

    elif cloud == "gcp":
        normalized["date"] = record.get("usage_start_time", "").split("T")[
            0] if "usage_start_time" in record else ""
        normalized["service"] = record.get("service.description", "")
        normalized["resource_id"] = record.get("resource.name", "")
        normalized["cost"] = float(record.get("cost", 0.0))
        normalized["account_id"] = record.get("project.id", "")
        normalized["region"] = record.get("location.region", "")
        normalized["usage_quantity"] = float(record.get("usage.amount", 0.0))
        normalized["usage_unit"] = record.get("usage.unit", "")

    elif cloud == "azure":
        normalized["date"] = record.get("Date", "")
        normalized["service"] = record.get("ServiceName", "")
        normalized["resource_id"] = record.get("ResourceId", "")
        normalized["cost"] = float(record.get("Cost", 0.0))
        normalized["account_id"] = record.get("SubscriptionId", "")
        normalized["region"] = record.get("ResourceLocation", "")
        normalized["usage_quantity"] = float(record.get("Quantity", 0.0))
        normalized["usage_unit"] = record.get("UnitOfMeasure", "")

    return normalized


def generate_consolidated_data(all_results):
    """
    Generate consolidated multi-cloud billing data.

    Args:
        all_results: Dictionary of results from all projects

    Returns:
        DataFrame with consolidated billing data
    """
    consolidated_records = []

    for project_name, project_results in all_results.items():
        for cloud, cloud_data in project_results.items():
            billing_data = cloud_data.get("billing_data", [])

            for record in billing_data:
                normalized = normalize_cloud_schema(
                    record, cloud, project_name)
                consolidated_records.append(normalized)

    if consolidated_records:
        return pd.DataFrame(consolidated_records)
    else:
        return pd.DataFrame()


def generate_cloud_distribution_report(df):
    """
    Generate report on cloud distribution across projects.

    Args:
        df: Consolidated DataFrame

    Returns:
        DataFrame with cloud distribution metrics
    """
    if df.empty:
        return pd.DataFrame()

    # Group by project and cloud
    distribution = df.groupby(['multi_cloud_project', 'cloud'])[
        'cost'].sum().reset_index()

    # Calculate total cost per project
    project_totals = df.groupby('multi_cloud_project')[
        'cost'].sum().reset_index()
    project_totals.columns = ['multi_cloud_project', 'total_cost']

    # Merge to get percentage
    distribution = distribution.merge(project_totals, on='multi_cloud_project')
    distribution['percentage'] = (
        distribution['cost'] / distribution['total_cost']) * 100

    return distribution


def generate_time_series_reports(df):
    """
    Generate time series reports for multi-cloud analysis.

    Args:
        df: Consolidated DataFrame

    Returns:
        Dictionary of time series DataFrames
    """
    if df.empty:
        return {}

    reports = {}

    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Monthly spend by cloud
    monthly_by_cloud = df.groupby([pd.Grouper(key='date', freq='ME'), 'cloud'])[
        'cost'].sum().reset_index()
    reports['monthly_by_cloud'] = monthly_by_cloud

    # Monthly spend by project and cloud
    monthly_by_project_cloud = df.groupby([pd.Grouper(
        key='date', freq='ME'), 'multi_cloud_project', 'cloud'])['cost'].sum().reset_index()
    reports['monthly_by_project_cloud'] = monthly_by_project_cloud

    # Service distribution across clouds
    service_distribution = df.groupby(['cloud', 'service'])[
        'cost'].sum().reset_index()
    reports['service_distribution'] = service_distribution

    return reports


def generate_migration_analysis(df, multi_cloud_projects):
    """
    Generate analysis specifically for migration scenarios.

    Args:
        df: Consolidated DataFrame
        multi_cloud_projects: Multi-cloud project configurations

    Returns:
        DataFrame with migration metrics
    """
    if df.empty:
        return pd.DataFrame()

    migration_data = []

    # Identify migration projects
    migration_projects = {
        name: config for name, config in multi_cloud_projects.items()
        if config['multi_cloud_pattern']['type'] == 'migration'
    }

    for project_name, config in migration_projects.items():
        pattern_params = config['multi_cloud_pattern'].get('params', {})
        source_cloud = pattern_params.get('source_cloud')
        target_cloud = pattern_params.get('target_cloud')

        if not source_cloud or not target_cloud:
            continue

        # Filter data for this project
        project_df = df[df['multi_cloud_project'] == project_name].copy()

        if project_df.empty:
            continue

        # Ensure date column is datetime
        project_df['date'] = pd.to_datetime(project_df['date'])

        # Get monthly data for source and target clouds
        monthly_data = project_df.groupby([pd.Grouper(key='date', freq='ME'), 'cloud'])[
            'cost'].sum().reset_index()

        # Pivot to have source and target as columns
        pivot_data = monthly_data.pivot(
            index='date', columns='cloud', values='cost').reset_index()

        # Calculate migration metrics
        if source_cloud in pivot_data.columns and target_cloud in pivot_data.columns:
            pivot_data['source_percentage'] = pivot_data[source_cloud] / \
                (pivot_data[source_cloud] + pivot_data[target_cloud]) * 100
            pivot_data['target_percentage'] = pivot_data[target_cloud] / \
                (pivot_data[source_cloud] + pivot_data[target_cloud]) * 100
            pivot_data['migration_progress'] = pivot_data['target_percentage']
            pivot_data['project'] = project_name

            # Add to migration data
            migration_data.append(pivot_data[[
                                  'date', 'project', 'source_percentage', 'target_percentage', 'migration_progress']])

    if migration_data:
        return pd.concat(migration_data)
    else:
        return pd.DataFrame()


def generate_multi_cloud_on_prem_comparison(df, multi_cloud_projects):
    """
    Generate comparison between cloud costs and estimated on-premises costs.

    Args:
        df: Consolidated DataFrame
        multi_cloud_projects: Multi-cloud project configurations

    Returns:
        DataFrame with cloud vs on-prem comparison
    """
    if df.empty or not DATA_VOLUME_SETTINGS["on_prem_cost_simulation"]:
        return pd.DataFrame()

    comparison_data = []

    # Look for repatriation scenarios specifically
    repatriation_projects = {
        name: config for name, config in multi_cloud_projects.items()
        if config['multi_cloud_pattern']['type'] == 'cloud_repatriation'
    }

    # Process repatriation projects
    for project_name, config in repatriation_projects.items():
        pattern_params = config['multi_cloud_pattern'].get('params', {})
        cloud_source = pattern_params.get('cloud_source')
        start_ratio = pattern_params.get('start_ratio', 0.3)

        if not cloud_source:
            continue

        # Filter data for this project
        project_df = df[df['multi_cloud_project'] == project_name].copy()

        if project_df.empty:
            continue

        # Ensure date column is datetime
        project_df['date'] = pd.to_datetime(project_df['date'])

        # Get monthly cloud costs
        monthly_cloud = project_df.groupby([pd.Grouper(key='date', freq='ME')])[
            'cost'].sum().reset_index()
        monthly_cloud['cost_type'] = 'cloud'

        # Generate estimated on-prem costs
        # For simplification, we'll use a factor of the cloud costs
        # Before repatriation: on-prem is higher (otherwise why move to cloud?)
        # After repatriation: on-prem is lower (that's why we're moving back)

        # Get the repatriation start date
        start_date = project_df['date'].min()
        total_days = (project_df['date'].max() - start_date).days
        repatriation_start = start_date + \
            datetime.timedelta(days=int(total_days * start_ratio))

        monthly_on_prem = monthly_cloud.copy()
        monthly_on_prem['cost_type'] = 'on_prem'

        # Adjust on-prem costs based on repatriation
        for idx, row in monthly_on_prem.iterrows():
            if row['date'] < repatriation_start:
                # Before repatriation: on-prem is higher than cloud
                monthly_on_prem.at[idx, 'cost'] = row['cost'] * 1.3
            else:
                # After repatriation starts: on-prem becomes lower than cloud
                # The savings ratio increases gradually to final target
                days_since_start = (row['date'] - repatriation_start).days
                progress_ratio = min(
                    1.0, days_since_start / (total_days * 0.3))
                final_savings_ratio = 0.7  # 30% savings with on-prem
                current_ratio = 1.3 - \
                    (1.3 - final_savings_ratio) * progress_ratio
                monthly_on_prem.at[idx, 'cost'] = row['cost'] * current_ratio

        # Combine cloud and on-prem data
        comparison = pd.concat([monthly_cloud, monthly_on_prem])
        comparison['project'] = project_name
        comparison_data.append(comparison)

    # Also add on-prem comparisons for other project types (optional)
    for project_name, config in multi_cloud_projects.items():
        if config['multi_cloud_pattern']['type'] == 'cloud_repatriation':
            continue  # Skip, already processed above

        # For non-repatriation projects, simulate simple on-prem costs
        # with a consistent cost ratio (usually higher than cloud)
        project_df = df[df['multi_cloud_project'] == project_name].copy()

        if project_df.empty:
            continue

        # Ensure date column is datetime
        project_df['date'] = pd.to_datetime(project_df['date'])

        # Get monthly cloud costs
        monthly_cloud = project_df.groupby([pd.Grouper(key='date', freq='ME')])[
            'cost'].sum().reset_index()
        monthly_cloud['cost_type'] = 'cloud'

        # Generate estimated on-prem costs (20-40% higher than cloud)
        on_prem_factor = random.uniform(1.2, 1.4)
        monthly_on_prem = monthly_cloud.copy()
        monthly_on_prem['cost_type'] = 'on_prem'
        monthly_on_prem['cost'] = monthly_on_prem['cost'] * on_prem_factor

        # Combine cloud and on-prem data
        comparison = pd.concat([monthly_cloud, monthly_on_prem])
        comparison['project'] = project_name
        comparison_data.append(comparison)

    if comparison_data:
        return pd.concat(comparison_data)
    else:
        return pd.DataFrame()


def generate_optimization_recommendations(df, multi_cloud_projects):
    """
    Generate optimization recommendations based on multi-cloud analysis.

    Args:
        df: Consolidated DataFrame
        multi_cloud_projects: Multi-cloud project configurations

    Returns:
        DataFrame with optimization recommendations
    """
    if df.empty:
        return pd.DataFrame()

    recommendations = []

    # 1. Identify potential migrations based on cost imbalances
    cloud_costs = df.groupby(['multi_cloud_project', 'cloud'])[
        'cost'].sum().reset_index()

    for project_name in cloud_costs['multi_cloud_project'].unique():
        project_costs = cloud_costs[cloud_costs['multi_cloud_project']
                                    == project_name]

        if len(project_costs) > 1:
            # Calculate cost ratios
            total_cost = project_costs['cost'].sum()
            for _, row in project_costs.iterrows():
                cloud = row['cloud']
                cost = row['cost']
                percentage = (cost / total_cost) * 100

                # Check for potential optimizations
                if percentage < 10 and cost > 0:
                    recommendations.append({
                        'project': project_name,
                        'recommendation_type': 'consolidation',
                        'cloud': cloud,
                        'description': f"Consider consolidating {cloud} workloads (only {percentage:.1f}% of project costs) to reduce multi-cloud overhead.",
                        'estimated_savings': cost * 0.3  # Estimate 30% savings from consolidation
                    })
                elif percentage > 80:
                    # Check if this is already a migration project
                    is_migration = False
                    if project_name in multi_cloud_projects:
                        pattern_type = multi_cloud_projects[project_name]['multi_cloud_pattern']['type']
                        is_migration = pattern_type == 'migration'

                    if not is_migration:
                        other_clouds = project_costs[project_costs['cloud'] != cloud]['cloud'].tolist(
                        )
                        if other_clouds:
                            recommendations.append({
                                'project': project_name,
                                'recommendation_type': 'evaluate_migration',
                                'cloud': cloud,
                                'description': f"Consider evaluating full migration to {cloud} (already {percentage:.1f}% of project costs).",
                                # Estimate 20% savings from migration
                                'estimated_savings': (total_cost - cost) * 0.2
                            })

    # 2. Identify potential RI/Savings Plan opportunities
    service_usage = df.groupby(['multi_cloud_project', 'cloud', 'service'])[
        'cost'].sum().reset_index()

    for _, row in service_usage.iterrows():
        project = row['project'] if 'project' in row else row['multi_cloud_project']
        cloud = row['cloud']
        service = row['service']
        cost = row['cost']

        # Check for high-cost compute services that might benefit from reservations
        compute_services = {
            'aws': ['EC2', 'RDS', 'ElastiCache', 'Redshift'],
            'azure': ['VirtualMachines', 'SQLDatabase', 'AKS'],
            'gcp': ['ComputeEngine', 'CloudSQL', 'GKE']
        }

        if cloud in compute_services and service in compute_services[cloud] and cost > 10000:
            recommendations.append({
                'project': project,
                'recommendation_type': 'reservation',
                'cloud': cloud,
                'service': service,
                'description': f"Consider purchasing reserved instances/commitments for {service} on {cloud}.",
                'estimated_savings': cost * 0.3  # Estimate 30% savings from reservations
            })

    # 3. Identify potential storage tier optimizations
    storage_services = {
        'aws': ['S3', 'EBS', 'EFS', 'Glacier'],
        'azure': ['BlobStorage', 'ManagedDisks', 'Files'],
        'gcp': ['CloudStorage', 'PersistentDisk', 'Filestore']
    }

    for cloud, services in storage_services.items():
        storage_costs = df[(df['cloud'] == cloud) &
                           (df['service'].isin(services))]
        if not storage_costs.empty:
            storage_grouped = storage_costs.groupby(['multi_cloud_project', 'service'])[
                'cost'].sum().reset_index()

            for _, row in storage_grouped.iterrows():
                project = row['multi_cloud_project']
                service = row['service']
                cost = row['cost']

                if cost > 5000:  # Significant storage cost
                    recommendations.append({
                        'project': project,
                        'recommendation_type': 'storage_tiering',
                        'cloud': cloud,
                        'service': service,
                        'description': f"Review {service} usage patterns for potential tiering optimizations.",
                        'estimated_savings': cost * 0.15  # Estimate 15% savings from storage optimization
                    })

    if recommendations:
        return pd.DataFrame(recommendations)
    else:
        return pd.DataFrame()


def save_results(all_results, consolidated_df, reports):
    """
    Save all generated data to output directory.

    Args:
        all_results: Raw results from all projects
        consolidated_df: Consolidated DataFrame
        reports: Dictionary of generated reports
    """
    # Create output directory structure
    create_output_directories()

    # Save raw cloud data
    for project_name, project_results in all_results.items():
        for cloud, cloud_data in project_results.items():
            # Save billing data
            billing_df = pd.DataFrame(cloud_data.get("billing_data", []))
            if not billing_df.empty:
                billing_df.to_csv(
                    f"{OUTPUT_DIR}/{cloud}/{project_name}_billing.csv", index=False)

            # Save tag data
            tags_df = pd.DataFrame(cloud_data.get("tag_data", []))
            if not tags_df.empty:
                tags_df.to_csv(
                    f"{OUTPUT_DIR}/{cloud}/{project_name}_tags.csv", index=False)

    # Save consolidated data
    if not consolidated_df.empty:
        consolidated_df.to_csv(
            f"{OUTPUT_DIR}/consolidated/all_clouds_billing.csv", index=False)

    # Save reports
    for report_name, report_df in reports.items():
        if not report_df.empty:
            report_df.to_csv(
                f"{OUTPUT_DIR}/consolidated/{report_name}.csv", index=False)


def generate_visualizations(reports):
    """
    Generate visualizations from the multi-cloud reports.

    Args:
        reports: Dictionary of report DataFrames
    """
    # Skip if reports are empty or pandas plotting is not available
    if not reports or not hasattr(pd.DataFrame, 'plot'):
        return

    try:
        import matplotlib.pyplot as plt

        # Set plot style
        plt.style.use('ggplot')

        # 1. Monthly cloud distribution
        if 'monthly_by_cloud' in reports:
            df = reports['monthly_by_cloud']
            if not df.empty:
                pivot_df = df.pivot(
                    index='date', columns='cloud', values='cost')
                fig, ax = plt.subplots(figsize=(12, 6))
                pivot_df.plot(kind='area', stacked=True, ax=ax)
                plt.title('Monthly Cost Distribution by Cloud')
                plt.xlabel('Date')
                plt.ylabel('Cost ($)')
                plt.savefig(
                    f"{OUTPUT_DIR}/visualizations/monthly_cloud_distribution.png")
                plt.close()

        # 2. Cloud distribution by project
        if 'cloud_distribution' in reports:
            df = reports['cloud_distribution']
            if not df.empty:
                for project in df['multi_cloud_project'].unique():
                    project_df = df[df['multi_cloud_project'] == project]
                    fig, ax = plt.subplots(figsize=(10, 6))
                    project_df.plot(kind='pie', y='percentage', labels=project_df['cloud'],
                                    autopct='%1.1f%%', ax=ax)
                    plt.title(f'Cloud Distribution for {project}')
                    plt.savefig(
                        f"{OUTPUT_DIR}/visualizations/{project}_cloud_distribution.png")
                    plt.close()

        # 3. Migration progress
        if 'migration_analysis' in reports:
            df = reports['migration_analysis']
            if not df.empty:
                for project in df['project'].unique():
                    project_df = df[df['project'] == project]
                    fig, ax = plt.subplots(figsize=(12, 6))
                    project_df.plot(x='date', y=['source_percentage', 'target_percentage'],
                                    kind='area', stacked=True, ax=ax)
                    plt.title(f'Migration Progress for {project}')
                    plt.xlabel('Date')
                    plt.ylabel('Percentage (%)')
                    plt.savefig(
                        f"{OUTPUT_DIR}/visualizations/{project}_migration_progress.png")
                    plt.close()

        # 4. Cloud vs On-Prem Comparison
        if 'cloud_vs_onprem' in reports:
            df = reports['cloud_vs_onprem']
            if not df.empty:
                for project in df['project'].unique():
                    project_df = df[df['project'] == project]
                    pivot_df = project_df.pivot(
                        index='date', columns='cost_type', values='cost')
                    fig, ax = plt.subplots(figsize=(12, 6))
                    pivot_df.plot(kind='line', marker='o', ax=ax)
                    plt.title(
                        f'Cloud vs On-Premises Cost Comparison for {project}')
                    plt.xlabel('Date')
                    plt.ylabel('Cost ($)')
                    plt.savefig(
                        f"{OUTPUT_DIR}/visualizations/{project}_cloud_vs_onprem.png")
                    plt.close()

        print(f"Visualizations saved to {OUTPUT_DIR}/visualizations/")

    except Exception as e:
        print(f"Error generating visualizations: {e}")
        print("Skipping visualization generation.")


def main():
    """Main function to coordinate multi-cloud data generation."""
    start_time = time.time()

    print("Multi-Cloud Cost and Usage Report Generator")
    print("===========================================")
    print("Data Volume Settings:")
    for key, value in DATA_VOLUME_SETTINGS.items():
        print(f"  {key}: {value}")

    # Create output directories
    create_output_directories()

    # Calculate budget
    annual_budget = calculate_annual_budget()
    print(f"Annual budget across all clouds: ${annual_budget:,.2f}")

    # Set date range for simulation
    days_to_generate = DATA_VOLUME_SETTINGS["days_to_generate"]
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_to_generate)
    print(
        f"Generating data for {days_to_generate} days from {start_date} to {end_date}")

    # Select projects to process
    projects_to_process = list(MULTI_CLOUD_PROJECTS.items())
    max_projects = DATA_VOLUME_SETTINGS["max_projects"]
    if len(projects_to_process) > max_projects:
        projects_to_process = random.sample(projects_to_process, max_projects)

    print(f"Processing {len(projects_to_process)} multi-cloud projects")

    # Prepare arguments for parallel processing
    project_args = []
    for project_name, project_config in projects_to_process:
        project_args.append((project_name, project_config,
                            start_date, end_date, annual_budget))

    # Process projects in parallel
    all_results = {}

    with multiprocessing.Pool(processes=min(len(project_args), multiprocessing.cpu_count())) as pool:
        results = pool.map(process_multi_cloud_project, project_args)

        for project_name, project_results in results:
            all_results[project_name] = project_results

    print(f"Generation completed for {len(all_results)} projects")

    # Generate consolidated data
    consolidated_df = generate_consolidated_data(all_results)
    print(
        f"Generated consolidated dataset with {len(consolidated_df)} records")

    # Generate reports
    reports = {}

    # Cloud distribution report
    cloud_distribution = generate_cloud_distribution_report(consolidated_df)
    reports['cloud_distribution'] = cloud_distribution

    # Time series reports
    time_series_reports = generate_time_series_reports(consolidated_df)
    reports.update(time_series_reports)

    # Migration analysis
    migration_analysis = generate_migration_analysis(
        consolidated_df, MULTI_CLOUD_PROJECTS)
    reports['migration_analysis'] = migration_analysis

    # Cloud vs On-Prem comparison
    cloud_vs_onprem = generate_multi_cloud_on_prem_comparison(
        consolidated_df, MULTI_CLOUD_PROJECTS)
    reports['cloud_vs_onprem'] = cloud_vs_onprem

    # Optimization recommendations
    optimization_recommendations = generate_optimization_recommendations(
        consolidated_df, MULTI_CLOUD_PROJECTS)
    reports['optimization_recommendations'] = optimization_recommendations

    # Save all results
    save_results(all_results, consolidated_df, reports)

    # Generate visualizations
    generate_visualizations(reports)

    end_time = time.time()
    print(
        f"Multi-cloud data generation completed in {end_time - start_time:.2f} seconds")
    print(f"Data saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
