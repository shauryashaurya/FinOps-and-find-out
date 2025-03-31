# GCP Billing Data: Practical Implementation Guide

## Table of Contents
- [SQL Query Examples](#sql-query-examples)
- [Data Processing Workflow](#data-processing-workflow)
- [Visualization Techniques](#visualization-techniques)
- [FinOps Implementation Patterns](#finops-implementation-patterns)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Multi-Cloud Integration](#multi-cloud-integration)

---

## SQL Query Examples

### Basic Cost Analysis Queries

#### Monthly Costs by Service
```sql
SELECT
  invoice.month,
  service.description,
  SUM(cost) AS total_cost
FROM
  `gcp_billing_export`
GROUP BY
  invoice.month, service.description
ORDER BY
  invoice.month, total_cost DESC;
```

#### Top 10 Expensive Projects
```sql
SELECT
  project.name,
  SUM(cost) AS total_cost
FROM
  `gcp_billing_export`
WHERE
  invoice.month = '2023-06'
GROUP BY
  project.name
ORDER BY
  total_cost DESC
LIMIT 10;
```

#### Cost Trends Over Time
```sql
SELECT
  invoice.month,
  SUM(cost) AS total_cost,
  SUM(CASE WHEN service.description = 'Compute Engine' THEN cost ELSE 0 END) AS compute_cost,
  SUM(CASE WHEN service.description = 'Cloud Storage' THEN cost ELSE 0 END) AS storage_cost,
  SUM(CASE WHEN service.description = 'BigQuery' THEN cost ELSE 0 END) AS bigquery_cost
FROM
  `gcp_billing_export`
GROUP BY
  invoice.month
ORDER BY
  invoice.month;
```

### Advanced Analysis Queries

#### Credit Analysis
```sql
SELECT
  invoice.month,
  JSON_EXTRACT_SCALAR(credit_item, '$.type') AS credit_type,
  SUM(CAST(JSON_EXTRACT_SCALAR(credit_item, '$.amount') AS FLOAT64)) AS credit_amount
FROM
  `gcp_billing_export`,
  UNNEST(JSON_EXTRACT_ARRAY(credits)) AS credit_item
GROUP BY
  invoice.month, credit_type
ORDER BY
  invoice.month, credit_amount;
```

#### Cost by Label
```sql
SELECT
  invoice.month,
  JSON_EXTRACT_SCALAR(project.labels, '$.environment') AS environment,
  JSON_EXTRACT_SCALAR(project.labels, '$.cost-center') AS cost_center,
  SUM(cost) AS total_cost
FROM
  `gcp_billing_export`
WHERE
  JSON_EXTRACT_SCALAR(project.labels, '$.environment') IS NOT NULL
GROUP BY
  invoice.month, environment, cost_center
ORDER BY
  invoice.month, total_cost DESC;
```

#### Tiered Pricing Analysis
```sql
WITH tiered_rates AS (
  SELECT
    service.description,
    JSON_EXTRACT_ARRAY(price.tiered_rates) AS rate_tiers
  FROM
    `gcp_billing_export`
  WHERE
    JSON_EXTRACT_ARRAY(price.tiered_rates) IS NOT NULL
  GROUP BY
    service.description, rate_tiers
)

SELECT
  service.description,
  JSON_EXTRACT_SCALAR(tier, '$.start_usage_amount') AS tier_start,
  JSON_EXTRACT_SCALAR(tier, '$.end_usage_amount') AS tier_end,
  JSON_EXTRACT_SCALAR(tier, '$.unit_price') AS unit_price,
  JSON_EXTRACT_SCALAR(tier, '$.unit') AS unit
FROM
  tiered_rates,
  UNNEST(rate_tiers) AS tier
ORDER BY
  service.description, tier_start;
```

### Chargeback/Showback Queries

#### Department Cost Allocation
```sql
SELECT
  invoice.month,
  JSON_EXTRACT_SCALAR(project.labels, '$.department') AS department,
  SUM(cost) AS total_cost,
  SUM(CASE 
        WHEN r.key = 'allocation-method' AND r.value = 'direct' 
        THEN e.cost 
        ELSE 0 
      END) AS direct_cost,
  SUM(CASE 
        WHEN r.key = 'allocation-method' AND r.value != 'direct' 
        THEN e.cost 
        ELSE 0 
      END) AS shared_cost
FROM
  `gcp_billing_export` e
LEFT JOIN
  `resource_labels` r
ON
  e.resource.name = r.resource_name
WHERE
  JSON_EXTRACT_SCALAR(project.labels, '$.department') IS NOT NULL
GROUP BY
  invoice.month, department
ORDER BY
  invoice.month, total_cost DESC;
```

#### Resource-Level Chargeback
```sql
SELECT
  e.invoice.month,
  e.project.name,
  r1.value AS chargeback_entity,
  r2.value AS cost_center,
  SUM(e.cost) AS total_cost
FROM
  `gcp_billing_export` e
JOIN
  `resource_labels` r1
ON
  e.resource.name = r1.resource_name AND r1.key = 'chargeback-entity'
LEFT JOIN
  `resource_labels` r2
ON
  e.resource.name = r2.resource_name AND r2.key = 'cost-center'
GROUP BY
  e.invoice.month, e.project.name, chargeback_entity, cost_center
ORDER BY
  e.invoice.month, total_cost DESC;
```

### Optimization Opportunity Queries

#### Underutilized Committed Use Discounts
```sql
SELECT
  invoice.month,
  project.name,
  service.description,
  SUM(cost) AS total_cost,
  SUM(CASE 
        WHEN JSON_EXTRACT_ARRAY(credits) IS NOT NULL 
        THEN ABS(CAST(JSON_EXTRACT_SCALAR(
            JSON_EXTRACT(JSON_EXTRACT_ARRAY(credits)[OFFSET(0)], '$')
          , '$.amount') AS FLOAT64))
        ELSE 0
      END) AS discount_amount,
  SUM(CASE 
        WHEN JSON_EXTRACT_ARRAY(credits) IS NOT NULL 
        THEN ABS(CAST(JSON_EXTRACT_SCALAR(
            JSON_EXTRACT(JSON_EXTRACT_ARRAY(credits)[OFFSET(0)], '$')
          , '$.amount') AS FLOAT64)) / cost * 100
        ELSE 0
      END) AS discount_percentage
FROM
  `gcp_billing_export`
WHERE
  service.description = 'Compute Engine'
GROUP BY
  invoice.month, project.name, service.description
HAVING
  discount_percentage < 30 AND total_cost > 1000
ORDER BY
  total_cost DESC;
```

#### Cost Anomaly Detection
```sql
WITH monthly_averages AS (
  SELECT
    project.name,
    AVG(cost) AS avg_daily_cost,
    STDDEV(cost) AS stddev_daily_cost
  FROM
    `gcp_billing_export`
  WHERE
    invoice.month >= '2023-03' AND invoice.month <= '2023-05' -- Historical period
  GROUP BY
    project.name
),
current_daily AS (
  SELECT
    DATE(usage_start_time) AS usage_date,
    project.name,
    SUM(cost) AS daily_cost
  FROM
    `gcp_billing_export`
  WHERE
    invoice.month = '2023-06' -- Current period
  GROUP BY
    usage_date, project.name
)

SELECT
  c.usage_date,
  c.project.name,
  c.daily_cost,
  m.avg_daily_cost,
  (c.daily_cost - m.avg_daily_cost) / m.stddev_daily_cost AS z_score
FROM
  current_daily c
JOIN
  monthly_averages m
ON
  c.project.name = m.project.name
WHERE
  ABS((c.daily_cost - m.avg_daily_cost) / m.stddev_daily_cost) > 2 -- Z-score threshold
  AND m.stddev_daily_cost > 0
ORDER BY
  ABS((c.daily_cost - m.avg_daily_cost) / m.stddev_daily_cost) DESC;
```

## Data Processing Workflow

### ETL Pipeline for Billing Data

Here's a recommended workflow for processing GCP billing data:

1. **Extract**: Collect raw billing data
   - Export to BigQuery (recommended)
   - Export to CSV files (if needed)

2. **Transform**: Process and enrich the data
   - Join with resource labels
   - Normalize project hierarchy
   - Apply allocation rules
   - Calculate derived metrics

3. **Load**: Store processed data
   - Create analytical tables
   - Build aggregated views
   - Generate reports

### Sample Airflow DAG Structure

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'finops',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcp_billing_processing',
    default_args=default_args,
    description='Process GCP billing data',
    schedule_interval='0 3 * * *',  # Run daily at 3 AM
)

# Extract billing data
extract_billing = BashOperator(
    task_id='extract_billing_data',
    bash_command='python /path/to/extract_billing.py --date {{ ds }}',
    dag=dag,
)

# Process resource labels
process_labels = BashOperator(
    task_id='process_resource_labels',
    bash_command='python /path/to/process_labels.py --date {{ ds }}',
    dag=dag,
)

# Apply allocation rules
apply_allocation = BashOperator(
    task_id='apply_allocation_rules',
    bash_command='python /path/to/apply_allocation.py --date {{ ds }}',
    dag=dag,
)

# Generate reports
generate_reports = BashOperator(
    task_id='generate_reports',
    bash_command='python /path/to/generate_reports.py --date {{ ds }}',
    dag=dag,
)

# Define task dependencies
extract_billing >> process_labels >> apply_allocation >> generate_reports
```

### Data Quality Checks

Implement these critical data quality checks:

1. **Completeness Check**
   ```sql
   -- Check if we have data for all projects
   SELECT
     invoice.month,
     COUNT(DISTINCT project.id) AS project_count,
     (SELECT COUNT(*) FROM `project_reference`) AS expected_project_count
   FROM
     `gcp_billing_export`
   WHERE
     invoice.month = '2023-06'
   GROUP BY
     invoice.month;
   ```

2. **Consistency Check**
   ```sql
   -- Check if costs align with expectations
   SELECT
     invoice.month,
     SUM(cost) AS total_cost,
     LAG(SUM(cost)) OVER (ORDER BY invoice.month) AS previous_month_cost,
     (SUM(cost) - LAG(SUM(cost)) OVER (ORDER BY invoice.month)) / 
       LAG(SUM(cost)) OVER (ORDER BY invoice.month) * 100 AS percent_change
   FROM
     `gcp_billing_export`
   GROUP BY
     invoice.month
   ORDER BY
     invoice.month;
   ```

3. **Anomaly Check**
   ```sql
   -- Detect suspiciously high costs
   SELECT
     DATE(usage_start_time) AS usage_date,
     project.name,
     service.description,
     SUM(cost) AS daily_cost,
     AVG(SUM(cost)) OVER (
       PARTITION BY project.name, service.description
       ORDER BY DATE(usage_start_time)
       ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
     ) AS avg_previous_7_days,
     SUM(cost) / AVG(SUM(cost)) OVER (
       PARTITION BY project.name, service.description
       ORDER BY DATE(usage_start_time)
       ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
     ) AS ratio_to_average
   FROM
     `gcp_billing_export`
   GROUP BY
     usage_date, project.name, service.description
   HAVING
     ratio_to_average > 3 AND daily_cost > 100
   ORDER BY
     ratio_to_average DESC;
   ```

## Visualization Techniques

### Key Visualizations for Cost Management

1. **Cost Trend Chart**
   - Time series of costs by month
   - Stacked by service or project
   - Include forecast line

2. **Cost Breakdown Treemap**
   - Hierarchical view of costs
   - Size = cost amount
   - Color = % change

3. **Service Distribution Pie Chart**
   - Distribution of costs by service
   - Highlight top 5 services
   - Group smaller services as "Other"

4. **Daily Heatmap**
   - Calendar view with costs by day
   - Color intensity = cost amount
   - Quickly identify spike days

### Looker Studio Dashboard Components

When building dashboards in Looker Studio (formerly Data Studio):

1. **Filter Controls**
   - Date range selector
   - Project dropdown
   - Service multi-select
   - Environment filter

2. **Summary Cards**
   - Month-to-date cost
   - Month-over-month % change
   - Projected month-end cost
   - Cost vs. budget percentage

3. **Trend Charts**
   - Line chart of daily costs
   - Stacked area chart of service costs
   - Bar chart of month-over-month comparison

4. **Breakdown Tables**
   - Project costs with filtering
   - Service costs with sorting
   - Label-based cost attribution

### Sample Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ □ Project  □ Date Range  □ Services                             │
├─────────────┬─────────────┬─────────────┬─────────────┐         │
│ MTD Cost    │ MoM Change  │ Forecast    │ vs Budget   │         │
│ $127,345    │ +12.5%      │ $198,420    │ 85%         │         │
├─────────────┴─────────────┴─────────────┴─────────────┘         │
├─────────────────────────────┬─────────────────────────────┐     │
│                             │                             │     │
│                             │                             │     │
│  Cost Trend Over Time       │  Service Breakdown          │     │
│  (Line Chart)               │  (Pie Chart)                │     │
│                             │                             │     │
│                             │                             │     │
├─────────────────────────────┼─────────────────────────────┤     │
│                             │                             │     │
│                             │                             │     │
│  Daily Cost Heatmap         │  Top Projects               │     │
│  (Calendar Heatmap)         │  (Bar Chart)                │     │
│                             │                             │     │
│                             │                             │     │
├─────────────────────────────┴─────────────────────────────┤     │
│                                                           │     │
│  Detailed Cost Table                                      │     │
│  (Table with Project, Service, Cost, MoM Change)          │     │
│                                                           │     │
└───────────────────────────────────────────────────────────┘     │
```

## FinOps Implementation Patterns

### Cost Allocation Framework

1. **Define Allocation Hierarchy**
   - Organization → Department → Team → Application → Environment

2. **Implement Tagging Strategy**
   - Required tags: environment, department, application, cost-center
   - Optional tags: team, owner, project
   - Enforcement mechanism: Cloud Asset Inventory

3. **Create Allocation Rules**
   - Direct costs: Assign based on resource labels
   - Shared costs: Distribute based on defined percentages
   - Network costs: Allocate based on usage pattern

### Budget Management Process

1. **Set Up Budget Hierarchy**
   - Organization-level budget
   - Department sub-budgets
   - Project-specific allocations

2. **Configure Alerting**
   - 50%, 75%, 90%, 100% thresholds
   - Daily burn rate alerts
   - Anomaly-based alerts

3. **Implement Review Cycle**
   - Weekly cost review meeting
   - Monthly budget reconciliation
   - Quarterly forecast adjustment

### Optimization Workflow

1. **Identify Opportunities**
   - Unused resources
   - Oversized instances
   - Storage optimization
   - Commitment discount gaps

2. **Prioritize Actions**
   - Sort by cost impact
   - Consider implementation effort
   - Evaluate business criticality

3. **Implement & Measure**
   - Document baseline costs
   - Implement changes
   - Measure actual savings
   - Document case studies

## Troubleshooting Common Issues

### Missing Cost Data

**Problem**: Cost data is incomplete for certain projects

**Debugging Steps**:
1. Check if the project exists in `project_lifecycle_mapping.csv`
2. Verify that the project ID is correctly formatted
3. Ensure the project is linked to a billing account
4. Check the date range for completeness

**Solution Example**:
```sql
-- Identify days with missing data
SELECT
  DATE(usage_start_time) AS date,
  COUNT(DISTINCT project.id) AS project_count
FROM
  `gcp_billing_export`
WHERE
  DATE(usage_start_time) BETWEEN '2023-06-01' AND '2023-06-30'
GROUP BY
  date
ORDER BY
  date;
```

### Reconciliation Discrepancies

**Problem**: Chargeback totals don't match original costs

**Debugging Steps**:
1. Verify all costs are allocated (check for unallocated)
2. Check for rounding errors in allocation percentages
3. Ensure no double-counting in allocation rules
4. Validate correct handling of credits and adjustments

**Solution Example**:
```sql
-- Compare original and allocated costs
SELECT
  original.invoice_month,
  original.total_cost AS original_total,
  allocated.total_cost AS allocated_total,
  original.total_cost - allocated.total_cost AS difference,
  (original.total_cost - allocated.total_cost) / original.total_cost * 100 AS percent_diff
FROM
  (SELECT invoice.month AS invoice_month, SUM(cost) AS total_cost
   FROM `gcp_billing_export`
   GROUP BY invoice.month) AS original
JOIN
  (SELECT invoice_month, SUM(allocated_cost) AS total_cost
   FROM `chargeback_by_entity`
   GROUP BY invoice_month) AS allocated
ON
  original.invoice_month = allocated.invoice_month
ORDER BY
  original.invoice_month;
```

### Label Inconsistencies

**Problem**: Inconsistent or missing labels causing allocation issues

**Debugging Steps**:
1. Identify resources with missing required labels
2. Check for inconsistent label values (case sensitivity, typos)
3. Look for resources with conflicting labels
4. Verify label inheritance is working as expected

**Solution Example**:
```sql
-- Find resources with missing critical labels
SELECT
  resource_name,
  COUNT(DISTINCT key) AS label_count,
  STRING_AGG(key, ', ') AS present_labels,
  CASE
    WHEN 'environment' NOT IN (SELECT key FROM `resource_labels` r WHERE r.resource_name = l.resource_name) THEN 'Missing environment'
    WHEN 'cost-center' NOT IN (SELECT key FROM `resource_labels` r WHERE r.resource_name = l.resource_name) THEN 'Missing cost-center'
    WHEN 'chargeback-entity' NOT IN (SELECT key FROM `resource_labels` r WHERE r.resource_name = l.resource_name) THEN 'Missing chargeback-entity'
    ELSE 'OK'
  END AS label_status
FROM
  `resource_labels` l
GROUP BY
  resource_name
HAVING
  label_status != 'OK'
ORDER BY
  label_count ASC;
```

## Multi-Cloud Integration

### Unified Schema Design

When integrating GCP with AWS and Azure, create a unified schema:

```sql
CREATE TABLE unified_cloud_costs (
  -- Common fields
  invoice_month STRING,
  usage_date DATE,
  cloud_provider STRING,  -- 'GCP', 'AWS', or 'Azure'
  
  -- Resource identification
  account_id STRING,        -- AWS account, GCP project, Azure subscription
  account_name STRING,      -- Human-readable name
  resource_id STRING,       -- Unique resource identifier
  resource_name STRING,     -- Human-readable resource name
  
  -- Service information
  service_category STRING,  -- Normalized service category
  service_name STRING,      -- Original service name
  service_detail STRING,    -- SKU or usage type
  
  -- Location
  region STRING,            -- Normalized region name
  cloud_region STRING,      -- Original cloud provider region
  zone STRING,              -- If available
  
  -- Cost information
  cost FLOAT64,             -- Cost in common currency (e.g., USD)
  original_cost FLOAT64,    -- Cost in original currency if different
  original_currency STRING, -- Original currency code
  discount_amount FLOAT64,  -- Discount amount (negative)
  discount_type STRING,     -- Type of discount applied
  
  -- Usage information
  usage_amount FLOAT64,     -- Amount of usage
  usage_unit STRING,        -- Unit of measure
  
  -- Business context
  business_unit STRING,
  cost_center STRING,
  environment STRING,
  application STRING,
  
  -- Original data
  source_data JSON          -- Original record for reference
);
```

### Cloud Provider Mapping Functions

Implement mapping functions for each cloud provider:

```python
def map_gcp_to_unified(gcp_record):
    """Map GCP billing record to unified schema."""
    project_labels = json.loads(gcp_record.get('project.labels', '{}'))
    
    return {
        'invoice_month': gcp_record.get('invoice.month'),
        'usage_date': parse_date(gcp_record.get('usage_start_time')),
        'cloud_provider': 'GCP',
        
        'account_id': gcp_record.get('project.id'),
        'account_name': gcp_record.get('project.name'),
        'resource_id': gcp_record.get('resource.name'),
        'resource_name': gcp_record.get('resource.name'),
        
        'service_category': map_gcp_service_to_category(gcp_record.get('service.description')),
        'service_name': gcp_record.get('service.description'),
        'service_detail': gcp_record.get('sku.description'),
        
        'region': normalize_region(gcp_record.get('location.region')),
        'cloud_region': gcp_record.get('location.region'),
        'zone': gcp_record.get('location.zone'),
        
        'cost': float(gcp_record.get('cost', 0)),
        'original_cost': float(gcp_record.get('cost', 0)),
        'original_currency': gcp_record.get('currency'),
        'discount_amount': extract_discount_amount(gcp_record.get('credits', '[]')),
        'discount_type': extract_discount_type(gcp_record.get('credits', '[]')),
        
        'usage_amount': float(gcp_record.get('usage.amount', 0)),
        'usage_unit': gcp_record.get('usage.unit'),
        
        'business_unit': project_labels.get('business-unit', ''),
        'cost_center': project_labels.get('cost-center', ''),
        'environment': project_labels.get('environment', ''),
        'application': project_labels.get('application', ''),
        
        'source_data': json.dumps(gcp_record)
    }
```

### Multi-Cloud Dashboard Strategy

When designing dashboards for multi-cloud environments:

1. **Use cloud-neutral metrics**
   - Total cost
   - Cost by business dimension
   - Unit economics (cost per transaction/user)

2. **Provide cloud-specific drill-downs**
   - Start with unified view
   - Allow drill-down to cloud-specific details
   - Include cloud-specific optimization recommendations

3. **Implement consistent dimensions**
   - Business unit
   - Environment
   - Application
   - Cost center

4. **Compare equivalent services**
   - Compute: EC2 vs Compute Engine vs VMs
   - Storage: S3 vs Cloud Storage vs Blob Storage
   - Database: RDS vs Cloud SQL vs SQL Database

### Sample Multi-Cloud Query

```sql
-- Cost comparison across clouds for similar services
SELECT
  invoice_month,
  cloud_provider,
  CASE
    WHEN service_name IN ('EC2', 'Compute Engine', 'Virtual Machines') THEN 'Compute'
    WHEN service_name IN ('S3', 'Cloud Storage', 'Blob Storage') THEN 'Object Storage'
    WHEN service_name IN ('RDS', 'Cloud SQL', 'SQL Database') THEN 'Managed SQL'
    WHEN service_name IN ('Lambda', 'Cloud Functions', 'Functions') THEN 'Serverless'
    WHEN service_name IN ('CloudFront', 'Cloud CDN', 'CDN') THEN 'CDN'
    ELSE 'Other'
  END AS unified_service,
  SUM(cost) AS total_cost,
  SUM(discount_amount) AS total_discount,
  SUM(cost) + SUM(discount_amount) AS pre_discount_cost,
  ROUND((SUM(discount_amount) / (SUM(cost) + SUM(discount_amount))) * -100, 2) AS discount_percentage
FROM
  unified_cloud_costs
WHERE
  invoice_month BETWEEN '2023-01' AND '2023-06'
GROUP BY
  invoice_month, cloud_provider, unified_service
ORDER BY
  invoice_month, unified_service, cloud_provider;
```
