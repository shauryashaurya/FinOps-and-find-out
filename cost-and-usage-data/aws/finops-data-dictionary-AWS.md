# FinOps Data Dictionary for AWS CUR Analysis with PySpark

## AWS CUR Data Model

### Primary Tables

#### 1. `cost_and_usage_report`
Contains the detailed AWS Cost and Usage Report data with line item details for all AWS services.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `identity/LineItemId` | String | Unique identifier for a line item | `li-0123456789abcdef0123456789abcdef` |
| `identity/TimeInterval` | String | Time period covered by this line item | `2023-10-01T00:00:00Z/2023-10-02T00:00:00Z` |
| `bill/InvoiceId` | String | ID of the invoice | `I-20231001` |
| `bill/BillingPeriodStartDate` | Timestamp | Billing period start date in UTC | `2023-10-01T00:00:00Z` |
| `bill/BillingPeriodEndDate` | Timestamp | Billing period end date in UTC | `2023-10-31T23:59:59Z` |
| `bill/PayerAccountId` | String | Account ID of the paying account | `111111111111` |
| `lineItem/UsageAccountId` | String | Account ID that used this line item | `222200000001` |
| `lineItem/LineItemType` | String | Type of charge | `Usage`, `Tax`, `DiscountedUsage` |
| `lineItem/UsageStartDate` | Timestamp | When the usage started | `2023-10-01T08:00:00Z` |
| `lineItem/UsageEndDate` | Timestamp | When the usage ended | `2023-10-01T16:00:00Z` |
| `lineItem/ProductCode` | String | AWS service code | `AmazonEC2`, `AmazonS3` |
| `lineItem/UsageType` | String | Type of usage | `USW2-BoxUsage:t2.micro` |
| `lineItem/Operation` | String | Specific AWS operation | `RunInstances` |
| `lineItem/AvailabilityZone` | String | Availability Zone | `us-west-2a` |
| `lineItem/ResourceId` | String | ID of the AWS resource | `i-0abc12345def67890` |
| `lineItem/UsageAmount` | Double | Amount of usage incurred | `8.0` |
| `lineItem/NormalizationFactor` | Double | Factor used to normalize EC2 usage | `0.5` |
| `lineItem/NormalizedUsageAmount` | Double | Normalized usage amount | `4.0` |
| `lineItem/CurrencyCode` | String | Currency code | `USD` |
| `lineItem/UnblendedRate` | Double | The actual rate charged | `0.0116` |
| `lineItem/UnblendedCost` | Double | The actual cost (UnblendedRate × UsageAmount) | `0.0928` |
| `lineItem/BlendedRate` | Double | Average rate across all accounts | `0.0125` |
| `lineItem/BlendedCost` | Double | BlendedRate × UsageAmount | `0.1000` |
| `lineItem/LineItemDescription` | String | Description of the line item | `$0.0116 per On Demand Linux t2.micro Instance Hour` |
| `product/ProductName` | String | Full name of the AWS service | `Amazon Elastic Compute Cloud` |
| `product/servicecode` | String | Code for the AWS service | `ec2` |
| `product/region` | String | AWS region | `us-west-2` |
| `pricing/unit` | String | Unit used to measure usage | `Hrs` |
| `pricing/publicOnDemandCost` | Double | On-Demand rate cost | `0.1000` |
| `pricing/term` | String | Term of the rate | `OnDemand` |
| `pricing/offeringClass` | String | For RI, class of offering | `Standard` |
| `reservation/ReservationARN` | String | ARN of the reservation (for RIs) | `arn:aws:ec2:us-west-2:123456789012:reserved-instances/...` |
| `reservation/NormalizedUnitsPerReservation` | Double | Normalized units per reservation | `1.0` |
| `savingsPlan/SavingsPlanARN` | String | ARN of the Savings Plan | `arn:aws:savingsplans::123456789012:savingsplan/...` |
| `savingsPlan/SavingsPlanRate` | Double | Rate for the Savings Plan | `0.0085` |
| `savingsPlan/UsedCommitment` | Double | Amount of commitment used | `10.25` |
| `savingsPlan/TotalCommitment` | Double | Total commitment amount | `100.0` |
| `month` | String | Year and month in YYYY-MM format | `2023-10` |
| `project` | String | Project name from resource tags | `SkyConnectPassengerApp` |
| `business_unit` | String | Business unit name | `Aviation` |
| `chargeback_entity` | String | Entity responsible for the cost | `IT` |
| `allocation_method` | String | Method used to allocate costs | `direct` |
| `cost_difference` | Double | BlendedCost - UnblendedCost | `0.0072` |
| `is_discounted` | Boolean | Whether the resource has a discount | `False` |

#### 2. `resource_tags`
Contains all metadata tags for AWS resources.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `resourceId` | String | ID of the AWS resource | `i-0abc12345def67890` |
| `key` | String | Tag key | `Environment` |
| `value` | String | Tag value | `Production` |

#### 3. `project_lifecycle_mapping`
Maps projects to their lifecycle patterns and provides additional metadata.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `project_name` | String | Name of the project | `SkyConnectPassengerApp` |
| `lifecycle` | String | Lifecycle pattern | `peak_and_plateau` |
| `business_unit` | String | Business unit that owns the project | `Aviation` |
| `use_case` | String | Primary use case | `Mobile Applications` |
| `description` | String | Project description | `Mobile application for airline passengers...` |
| `stages` | String | Deployment stages (comma-separated) | `aviation-prod, aviation-dev` |
| `services` | String | AWS services used (comma-separated) | `Lambda, DynamoDB, APIGateway...` |

### Summary Tables

#### 4. `cost_summary_by_project`
Monthly costs aggregated by project.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `month` | String | Year and month in YYYY-MM format | `2023-10` |
| `project` | String | Project name | `SkyConnectPassengerApp` |
| `lineItem/UnblendedCost` | Double | Total unblended cost | `4275.62` |

#### 5. `cost_summary_by_service`
Monthly costs aggregated by AWS service.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `month` | String | Year and month in YYYY-MM format | `2023-10` |
| `lineItem/ProductCode` | String | AWS service code | `AmazonEC2` |
| `lineItem/UnblendedCost` | Double | Total unblended cost | `12840.56` |

#### 6. `cost_summary_by_business_unit`
Monthly costs aggregated by business unit.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `month` | String | Year and month in YYYY-MM format | `2023-10` |
| `business_unit` | String | Business unit name | `Aviation` |
| `lineItem/UnblendedCost` | Double | Total unblended cost | `28750.10` |

## FinOps Framework KPIs

### Cost Allocation Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Fully Allocated Costs** | Total costs allocated to cost centers | Sum of unblended costs with complete allocation | Currency (USD) |
| **Cost Allocation Coverage** | Percentage of costs allocated to projects/teams | (Allocated Costs / Total Costs) × 100 | Percentage |
| **Unallocated Costs** | Costs not allocated to any cost center | Sum of costs without project tags | Currency (USD) |
| **Cost per Business Unit** | Total cost by business unit | Sum of costs grouped by business unit | Currency (USD) |
| **Cost per Project** | Total cost by project | Sum of costs grouped by project | Currency (USD) |
| **Cost per Service** | Total cost by AWS service | Sum of costs grouped by service | Currency (USD) |
| **Cost per Account** | Total cost by AWS account | Sum of costs grouped by account | Currency (USD) |
| **Tag Compliance Rate** | Percentage of resources with required tags | (Resources with Tag / Total Resources) × 100 | Percentage |

### Unit Economics Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Cost per Transaction** | Cost per business transaction | Total Cost / Number of Transactions | Currency (USD) |
| **Cost per User** | Cost per active user | Total Cost / Number of Active Users | Currency (USD) |
| **Revenue to Cloud Cost Ratio** | Revenue compared to cloud costs | Revenue / Total Cloud Cost | Ratio |
| **Profit Margin Impact** | Cloud cost impact on profit margins | (Cloud Cost / Revenue) × 100 | Percentage |
| **Unit Cost Trending** | Change in cost per unit over time | (Current Period Unit Cost / Previous Period Unit Cost) - 1 | Percentage |

### Resource Utilization Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **EC2 Instance Utilization** | EC2 instance CPU utilization | Average CPU utilization per instance | Percentage |
| **Idle Resource Cost** | Cost of underutilized resources | Sum of costs for instances with utilization < threshold | Currency (USD) |
| **Overprovisioned Resources** | Resources with excess capacity | Count of instances with utilization < threshold | Count |
| **Right-Sizing Savings Opportunity** | Potential savings from right-sizing | Sum of cost difference between current and right-sized resources | Currency (USD) |
| **Utilization Efficiency Score** | Composite score of resource utilization | Weighted average of utilization metrics | Score (0-100) |

### Commitment-Based Discount Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Savings Plan Coverage** | Percentage of eligible usage covered by Savings Plans | (SP Covered Cost / Eligible On-Demand Cost) × 100 | Percentage |
| **Savings Plan Utilization** | Utilization of purchased Savings Plans | (SP Used Commitment / SP Total Commitment) × 100 | Percentage |
| **Reserved Instance Coverage** | Percentage of eligible usage covered by RIs | (RI Covered Cost / Eligible On-Demand Cost) × 100 | Percentage |
| **Reserved Instance Utilization** | Utilization of purchased RIs | (RI Used Hours / RI Total Hours) × 100 | Percentage |
| **Commitment Discount Savings** | Total savings from commitment-based discounts | On-Demand Equivalent Cost - Actual Cost | Currency (USD) |
| **Commitment Opportunity** | Potential additional savings from commitments | Estimated savings from additional commitments | Currency (USD) |

### Cost Anomaly Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Cost Variance** | Variance from expected costs | (Actual Cost - Expected Cost) / Expected Cost × 100 | Percentage |
| **Cost Growth Rate** | Month-over-month cost growth | (Current Month Cost / Previous Month Cost) - 1 | Percentage |
| **Budget Attainment** | Actual costs compared to budget | (Actual Cost / Budgeted Cost) × 100 | Percentage |
| **Anomaly Count** | Number of cost anomalies detected | Count of costs exceeding thresholds | Count |
| **Cost Spike Severity** | Severity of cost spikes | Max(Cost Variance) | Percentage |

### Forecasting Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Cost Forecast Accuracy** | Accuracy of cost forecasts | (Actual Cost - Forecasted Cost) / Actual Cost × 100 | Percentage |
| **Projected Annual Cost** | Projected cost for the year | Sum of actual costs + forecasted costs | Currency (USD) |
| **Forecast Variance** | Variance between forecasts over time | Standard deviation of forecasts | Currency (USD) |
| **Cost Trend Indicator** | Direction and strength of cost trend | Slope of the cost trend line | Currency/Month |

### Optimization Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Cost Optimization Savings** | Savings from optimization actions | Sum of savings from all optimization actions | Currency (USD) |
| **Optimization ROI** | Return on investment for optimization efforts | Savings / Cost of Optimization Efforts | Ratio |
| **Waste Reduction** | Reduction in wasted resources | (Previous Waste - Current Waste) / Previous Waste × 100 | Percentage |
| **Optimization Coverage** | Percentage of resources reviewed for optimization | (Resources Reviewed / Total Resources) × 100 | Percentage |
| **Optimization Impact** | Impact of optimizations on total cost | (Optimization Savings / Total Cost) × 100 | Percentage |

### Lifecycle-Based Metrics

| KPI | Description | Calculation Approach | Unit |
|-----|-------------|----------------------|------|
| **Lifecycle Cost Trajectory** | Cost trajectory based on lifecycle pattern | Rolling average of costs compared to expected lifecycle pattern | Score (-1 to 1) |
| **Lifecycle Phase Indicator** | Current phase in the project lifecycle | Classification based on cost patterns | Category |
| **Growth Rate by Lifecycle** | Growth rate grouped by lifecycle category | Average growth rate for projects in each lifecycle | Percentage |
| **Lifecycle Cost Efficiency** | Cost efficiency relative to lifecycle expectations | Actual cost / Expected cost for lifecycle phase | Ratio |

## Data Relationships and Join Keys

| Relationship | Primary Table | Primary Key | Foreign Table | Foreign Key |
|--------------|--------------|-------------|---------------|------------|
| Resource to Tags | `cost_and_usage_report` | `lineItem/ResourceId` | `resource_tags` | `resourceId` |
| Cost to Project | `cost_and_usage_report` | `project` | `project_lifecycle_mapping` | `project_name` |
| Resource to Account | `cost_and_usage_report` | `lineItem/UsageAccountId` | `account_hierarchy` | `account_id` |

## Common Data Transformations for PySpark

1. **Date transformations**:
   - Extract year, month, day from timestamp fields
   - Group by various time periods (day, week, month, quarter)
   - Calculate month-over-month and year-over-year comparisons

2. **Cost normalization**:
   - Normalize costs across different time periods (30-day normalization)
   - Adjust for varying month lengths
   - Apply currency conversion if needed

3. **Aggregations**:
   - Sum costs by various dimensions (account, service, region, etc.)
   - Calculate averages, minimum, maximum
   - Use window functions for moving averages and cumulative sums

4. **Joining strategies**:
   - Join CUR data with tag data using resource ID
   - Join with project metadata using project name
   - Join with account hierarchy for organization structure

5. **Pattern detection**:
   - Detect usage patterns with window functions
   - Identify anomalies using statistical methods
   - Classify spending patterns using lifecycle information

## Schema Evolution Handling

1. **Column additions**:
   - AWS regularly adds new columns to CUR
   - Use schema_on_read or schema evolution capabilities

2. **Tag handling**:
   - Tags can change over time
   - Store tag history for time-based analysis

3. **Service updates**:
   - New AWS services may appear in the data
   - Handle unknown service codes gracefully

## Performance Considerations

1. **Partitioning strategies**:
   - Partition by year and month for efficient queries
   - Consider partitioning by account ID for large organizations

2. **Data skew handling**:
   - Some accounts or services may have significantly more data
   - Use salting or repartitioning for heavy hitters

3. **Caching strategies**:
   - Cache frequently accessed reference data
   - Consider materializing common aggregations

4. **Optimization techniques**:
   - Use broadcast joins for dimension tables
   - Apply predicate pushdown where possible
   - Consider Adaptive Query Execution
