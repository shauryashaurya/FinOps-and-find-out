# Multi-Cloud Billing Data Generator

This tool generates synthetic billing data for multi-cloud environments spanning AWS, GCP, and Azure. It builds upon the existing cloud-specific generators to simulate various cloud deployment scenarios including migrations, expansions, consolidations, disaster recovery, and more.

## Prerequisites

- Python 3.7+
- Pandas
- NumPy
- Matplotlib (optional, for visualizations)
- Existing single-cloud billing generators:
  - `aws_cur_data_generator.py` and `aws_config.py`
  - `GCP_billing_data_generator.py` and `configGCP.py`
  - `Azure-billing-data-generator.py` and `configAzure.py`

## Installation

1. Ensure all prerequisites are installed:
```bash
pip install pandas numpy matplotlib
```

2. Place the `multi-cloud-billing-generator.py` file in the same directory as the single-cloud generators.

3. Create or modify `config_multi_cloud.py` with your desired multi-cloud project configurations.

## Usage

Run the generator with:

```bash
python multi-cloud-billing-generator.py
```

By default, this will:
1. Process multi-cloud projects defined in `config_multi_cloud.py`
2. Generate billing data for each cloud platform
3. Create consolidated reports and visualizations
4. Save all data to the `output/multi-cloud/` directory

### Output Directory Structure

```
output/multi-cloud/
├── aws/                   # Raw AWS billing data by project
├── gcp/                   # Raw GCP billing data by project
├── azure/                 # Raw Azure billing data by project
├── consolidated/          # Consolidated reports across clouds
│   ├── all_clouds_billing.csv          # Normalized billing data
│   ├── cloud_distribution.csv          # Cloud distribution by project
│   ├── monthly_by_cloud.csv            # Monthly spend by cloud
│   ├── monthly_by_project_cloud.csv    # Monthly spend by project and cloud
│   ├── migration_analysis.csv          # Migration progress metrics
│   ├── cloud_vs_onprem.csv             # Cloud vs on-prem comparison
│   └── optimization_recommendations.csv # Cost optimization suggestions
└── visualizations/        # Generated charts and graphs
```

## Configuration

### Multi-Cloud Project Configuration Format

Define projects in `config_multi_cloud.py` using the following structure:

```python
MULTI_CLOUD_PROJECTS = {
    "ProjectName": {
        "description": "Project description",
        "use_case": "Enterprise Applications",
        "business_unit": "Finance",
        "multi_cloud_pattern": {
            "type": "steady_state",  # or migration, expansion, consolidation, etc.
            "params": {}  # Pattern-specific parameters
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": ["EC2", "RDS", "Lambda"],
                "stages": ["softwaresolutions-prod"],
                "percentage": 0.7  # Distribution percentage
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": ["VirtualMachines", "SQLDatabase"],
                "stages": ["ml-prod"],
                "percentage": 0.3
            }
        }
    }
}
```

### Multi-Cloud Patterns

The generator supports several multi-cloud patterns:

1. **steady_state** - Stable distribution across multiple clouds
2. **migration** - Gradual transition from one cloud to another
3. **expansion** - Adding a new cloud platform over time
4. **consolidation** - Reducing the number of cloud platforms over time
5. **dr_scenario** - Primary and DR cloud with periodic DR testing
6. **burst_scaling** - Using secondary cloud for overflow capacity
7. **cloud_repatriation** - Moving workloads back from public cloud to on-premises

Each pattern requires specific parameters in the `params` section.

### Data Volume Settings

Edit the `DATA_VOLUME_SETTINGS` dictionary in `multi-cloud-billing-generator.py` to control data generation:

```python
DATA_VOLUME_SETTINGS = {
    "days_to_generate": 365,           # Number of days to generate data for
    "sampling_interval": 3,            # Generate data every X days
    "on_prem_cost_simulation": True,   # Generate simulated on-premises costs
    "volatility_factor": 0.02,         # Cost volatility factor
    "max_projects": 10,                # Maximum number of projects to process
}
```

## Example Multi-Cloud Scenarios

The sample configuration includes examples like:

1. **FinancialServicesHybrid** - Core banking in AWS with analytics in Azure
2. **RetailPlatformMigration** - E-commerce platform migrating from AWS to GCP
3. **HealthcareTriCloudAnalytics** - Healthcare analytics across all three clouds
4. **DisasterRecoverySetup** - Manufacturing systems with Azure primary and AWS DR
5. **CloudRepatriationProject** - Finance applications moving from cloud back to on-premises
6. **SecurityComplianceMultiCloud** - Centralized security spanning all cloud platforms

## Reports and Visualizations

The generator produces several reports to facilitate multi-cloud analysis:

1. **Cloud Distribution** - How costs are distributed across clouds for each project
2. **Monthly Trends** - Time series data showing spending patterns
3. **Migration Analysis** - Progress metrics for migration scenarios
4. **Cloud vs On-Prem** - Comparison with estimated on-premises costs
5. **Optimization Recommendations** - Automated cost optimization suggestions

## Extending the Generator

To add new multi-cloud patterns:

1. Define the pattern in `MULTI_CLOUD_PATTERNS` at the top of the file
2. Implement a handler function in `apply_multi_cloud_lifecycle()`
3. Update the project configuration to use the new pattern

## Troubleshooting

If you encounter errors:

1. Check that all required single-cloud generators are in the same directory
2. Verify that your project configurations use valid cloud services from the single-cloud configs
3. Ensure that the stages referenced in your projects exist in the single-cloud configs
4. Check the console output for specific error messages during generation

## Contributing

Feel free to extend and customize this generator for your specific multi-cloud scenarios. Consider contributing new patterns, visualizations, or reporting capabilities back to the project.
