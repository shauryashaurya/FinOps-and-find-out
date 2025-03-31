# Azure Cost Management Data Dictionary and FinOps Guide

## Data Dictionary for Azure Cost Management Export

The generated Azure Cost Management data contains the following columns, matching the official schema for Azure Cost Management exports to CSV and other storage destinations.

| Column Name | Data Type | Description | Example Value | Notes |
|-------------|-----------|-------------|--------------|-------|
| BillingAccountId | String | Unique identifier for the billing account | 01A2B3-C4D5E6-F7G8H9 | Typically an Enterprise Agreement, MCA, or Partner agreement ID |
| BillingAccountName | String | Display name of the billing account | Primary Billing Account | Name as it appears in the Azure portal |
| BillingPeriodStartDate | Date | Start date of the billing period | 2023-03-01 | YYYY-MM-DD format |
| BillingPeriodEndDate | Date | End date of the billing period | 2023-03-31 | YYYY-MM-DD format |
| BillingProfileId | String | Identifier for the billing profile (in MCA) | billing-profile-01A2B3 | May be empty for EA customers |
| BillingProfileName | String | Name of the billing profile | Enterprise Agreement | For EA, typically "Enterprise Agreement" |
| AccountOwnerId | String | ID of the account owner | owner-12345678 | References the Azure AD account |
| AccountName | String | Name of the account or department | Manufacturing | Often maps to business unit |
| SubscriptionId | GUID | Unique ID of the Azure subscription | 00000000-0000-0000-0000-000444400001 | 36-character GUID |
| SubscriptionName | String | Display name of the subscription | Manufacturing Production | Name as configured in Azure |
| Date | Date | Usage date | 2023-03-15 | The date when the resource was used (YYYY-MM-DD) |
| Product | String | Azure product or service used | VirtualMachines | High-level product category |
| PartNumber | String | Part number for the product/service | Part-E132-61 | Used for internal tracking |
| MeterId | String | Unique identifier for the meter | F3DB-E132-6157 | Used to identify the specific meter |
| ServiceFamily | String | Service category | Compute | Top-level Azure service family |
| MeterCategory | String | Category of the meter | VirtualMachines | The service category for the meter |
| MeterSubCategory | String | Subcategory of the meter | Standard | More specific meter category |
| MeterName | String | Name of the meter | Virtual Machines Compute Hours in eastus | Descriptive name of what's being measured |
| MeterRegion | String | Region where the resource is deployed | eastus | Azure region name |
| UnitOfMeasure | String | Unit used for billing this resource | Hour | How usage is measured (Hour, GB, etc.) |
| Quantity | Decimal | Amount of usage in the specified unit | 24.5 | Amount of resources consumed |
| EffectivePrice | Decimal | Price per unit after discounts | 0.0465 | The rate charged per unit after any discounts |
| Cost | Decimal | Total cost for this line item | 1.13925 | Quantity × EffectivePrice |
| CostInBillingCurrency | Decimal | Cost in the billing currency | 1.13925 | May differ from Cost if currency differs |
| CostCenter | String | Cost center from tags or organizational structure | Manufacturing-1234 | Often sourced from resource tags |
| ResourceLocation | String | Azure region of the resource | eastus | Region where resource is deployed |
| ConsumedService | String | The Azure service consumed | Microsoft.Compute | Resource provider name |
| ResourceId | String | Full Azure Resource Manager ID | /subscriptions/00000000-0000-0000-0000-000444400001/resourceGroups/vm-rg/providers/Microsoft.Compute/virtualMachines/mfg-web-prod-s-1234 | Hierarchical ID that uniquely identifies the resource |
| ResourceName | String | Name of the resource | mfg-web-prod-s-1234 | The resource name without the full path |
| ServiceName | String | Name of the service | VirtualMachines | Service name for the resource |
| ServiceTier | String | Tier of the service | Standard | Standard, Premium, Basic, etc. |
| ResourceGroupName | String | Name of the resource group | vm-rg | Resource group containing the resource |
| ResourceType | String | Type of resource | Microsoft.Compute/virtualMachines | ARM resource type |
| PublisherType | String | Type of publisher | Microsoft | Typically "Microsoft" for first-party services |
| PublisherName | String | Name of publisher | Microsoft | Name of the service publisher |
| ReservationId | String | ID of the reserved instance | RI-12345678 | Only populated for resources using RIs |
| ReservationName | String | Name of the reservation | Reserved Instance: 1 year | Description of the reservation |
| ProductOrderId | String | ID of the product order | RI-Order-123456 | Order ID for purchases like RIs |
| ProductOrderName | String | Name of the product order | Annual Reserved Instance Purchase | Description of the product order |
| OfferId | String | Azure offer ID | MS-AZR-0017P | Code representing the type of Azure offer (EA, Pay-As-You-Go, etc.) |
| BenefitId | String | ID of the benefit | AHB-12345678 | Identifies specific discount benefit |
| BenefitName | String | Name of the benefit | Azure Hybrid Benefit | Description of the applied benefit |
| Term | String | Term of commitment | P1Y | ISO 8601 duration (P1Y = 1 year) |
| CostAllocationRuleName | String | Name of cost allocation rule | ProportionalUsage-ITServices | For distributed shared costs |
| Tags | JSON String | Resource tags as a JSON string | {"environment":"production","business-unit":"Manufacturing"} | Key-value pairs from Azure resource tags |
| AdditionalInfo | JSON String | Additional service-specific details | {"serviceInfo":"VirtualMachines Compute Hours",...} | JSON object with extra metadata |
| ServiceInfo1 | String | Service-specific information field 1 | VirtualMachines Compute Hours | Service details |
| ServiceInfo2 | String | Service-specific information field 2 | Virtual Machines Compute Hours in eastus | Additional service details |
| PricingModel | String | Pricing model used | reservation | on_demand, reservation, savings_plan, etc. |
| ChargeType | String | Type of charge | Usage | Usage, Tax, Adjustment, etc. |
| Frequency | String | Frequency of the charge | Recurring | Recurring, OneTime, etc. |
| PricingCurrency | String | Currency used for pricing | USD | ISO currency code |

## Azure Cost Management and FinOps

### Azure Cost Management Overview

Azure Cost Management is Microsoft's native cost management solution that helps organizations monitor, allocate, and optimize their Azure cloud spending. It provides tools for cost analysis, budgeting, anomaly detection, cost allocation, and generating recommendations for optimizing Azure resources.

### How Azure Cost and Usage Operations Work

1. **Data Collection**: 
   - Usage data is collected from all Azure resources within a subscription
   - Data is processed by the Azure commerce system
   - Usage is rated (priced) based on the rates for your specific Azure offer

2. **Export Options**:
   - Data can be viewed in the Azure portal
   - Exports can be scheduled to Azure Storage, Event Hubs, or Log Analytics
   - Supported formats include CSV and JSON
   - Exports can contain detailed daily or monthly data

3. **Data Latency**:
   - Usage data typically has a latency of 8-24 hours
   - Cost data may have additional processing time
   - Amortized RI data becomes available after a few days into the month

4. **Data Retention**:
   - In the portal: 13-36 months depending on your agreement type
   - When exported: Controlled by your storage settings and retention policies

### Chargeback and Showback in Azure Context

**Showback**:
- Uses Azure Cost Management data to provide visibility into costs without directly charging teams
- Implemented using resource tags, resource groups, subscriptions, and management groups
- Can leverage cost allocation rules for shared services
- Often used with Azure Tags for departmental showback reports

**Chargeback**:
- Direct invoicing of business units or teams based on their Azure resource usage
- Typically requires additional tools or processes beyond native Azure capabilities
- Can be implemented using exports to financial systems
- Uses cost data from:
  - Resource tags (key-value metadata)
  - Resource groups (logical containers)
  - Subscriptions (billing boundaries)
  - Management groups (hierarchical organization)

**Cost Allocation**:
- Azure Cost Allocation rules (preview) enable splitting shared costs across multiple resources
- Types of allocation methods:
  1. **Proportional**: Split costs based on proportional consumption of a selected metric
  2. **Fixed**: Split costs based on fixed percentages defined by you
  3. **Even split**: Divides costs equally among all targets

### Azure-Specific FinOps Features vs GCP/AWS

#### Unique to Azure

1. **Reserved Instances Structure**:
   - Azure RIs are subscription-scoped by default
   - Can be assigned to a specific subscription or shared
   - More flexible than AWS RIs (which are region-specific)
   - Less complex than GCP CUDs (which are project-specific)

2. **Azure Hybrid Benefit (AHB)**:
   - Unique licensing benefit for existing Microsoft customers
   - Allows reuse of Windows Server and SQL Server licenses in Azure
   - Can provide up to 40-47% savings on VMs and SQL Database
   - Has no direct equivalent in AWS or GCP

3. **EA Portal vs. Azure Portal Duality**:
   - Enterprise customers manage billing through EA Portal
   - Resource management through Azure Portal
   - Creates a split management experience not present in AWS or GCP

4. **Management Group Hierarchies**:
   - More flexible than AWS Organizations
   - Can create custom hierarchies for policy inheritance and cost reporting
   - Up to 6 levels deep (root + 5 levels)

5. **DevTest Pricing Benefits**:
   - Special pricing for development and testing environments
   - Not available on all enterprise plans
   - Roughly equivalent to AWS Dev environments but more formalized

#### Differences from AWS

1. **Billing Structure**:
   - Azure uses EA/MCA/CSP models vs AWS's consolidated billing
   - Azure billing accounts can have multiple billing profiles (MCA)
   - Azure has management groups above subscriptions; AWS has OUs above accounts

   **Detailed Comparison of Azure and AWS Billing Models:**

   **Azure's Three Primary Billing Models:**

   1. **EA (Enterprise Agreement)**
      - **Structure**: Enterprise → Departments → Accounts → Subscriptions
      - **Key Features**:
        - Requires monetary commitment upfront (typically 3-year agreements)
        - Pricing based on committed spend levels (higher commitment = deeper discounts)
        - Administered through a separate EA Portal (not the Azure Portal)
        - Department-level budget tracking and spending caps
        - Enrollment administrators manage accounts and departments
      - **Best For**: Large enterprises with predictable Azure spending

   2. **MCA (Microsoft Customer Agreement)**
      - **Structure**: Billing Account → Billing Profiles → Invoice Sections → Subscriptions
      - **Key Features**:
        - Microsoft's newer model that's replacing EA for many customers
        - No minimum commitment required
        - Self-service management through Azure portal (no separate portal)
        - More granular billing management with Invoice Sections
        - Allows different payment methods for different parts of the organization
        - Monthly invoices with flexible payment terms
      - **Best For**: Organizations needing more billing flexibility or department-specific payment methods

   3. **CSP (Cloud Solution Provider)**
      - **Structure**: Partner → Customer Tenants → Subscriptions
      - **Key Features**:
        - Microsoft partner manages the billing relationship
        - Customer receives one bill from the partner, not Microsoft
        - Partner may provide additional services, support, and customized billing
        - Often includes value-added services from the partner
        - Limited direct visibility into actual Microsoft rates
      - **Best For**: Organizations preferring a managed relationship with a Microsoft partner

   **AWS Consolidated Billing**

   - **Structure**: Organizations → Organizational Units → Accounts
   - **Key Features**:
     - Single payment model for all customer types
     - One payer account responsible for all charges
     - All linked accounts roll up to the payer account
     - Usage aggregated across accounts for volume discounts
     - Reserved Instances and Savings Plans automatically shared
     - Consistent experience regardless of company size
     - No separate portals for different aspects of billing

   **Key Differences and Implications**

   1. **Agreement Complexity**:
      - Azure billing often integrated with broader Microsoft licensing (like Office 365)
      - AWS has a simpler, cloud-focused approach

   2. **Portal Experience**:
      - Azure EA customers must use two different portals (EA Portal for billing, Azure Portal for resources)
      - AWS provides a unified experience in a single console

   3. **Billing Flexibility**:
      - Azure offers three different models to choose from based on your needs
      - AWS offers one model with internal flexibility through Organizations

   4. **Cost Allocation**:
      - Azure: Tags, Resource Groups, Management Groups, Subscriptions
      - AWS: Tags, Accounts, Organizational Units

   5. **Migration Between Models**:
      - Moving between Azure billing models (e.g., EA to MCA) can be complex
      - AWS model remains consistent as your organization grows

2. **Savings Plans Approach**:
   - Azure Savings Plans are newer and less flexible than AWS
   - AWS offers Compute, EC2 Instance, and SageMaker Savings Plans
   - Azure's are limited to specific service families

3. **Cost Allocation Tags**:
   - AWS distinguishes between user-defined and AWS-generated tags
   - AWS requires explicit activation of tags for cost reporting
   - Azure uses all resource tags in cost reporting automatically

#### Differences from GCP

1. **Billing Hierarchy**:
   - GCP uses Projects → Folders → Organization
   - Azure uses Resources → Resource Groups → Subscriptions → Management Groups → Tenant
   - Azure subscriptions are more rigid billing boundaries than GCP projects

2. **Discount Models**:
   - GCP uses Committed Use Discounts (CUDs) vs Azure's RIs and Savings Plans
   - GCP provides automatic sustained use discounts not available in Azure
   - GCP offers custom flat-rate pricing for high-volume customers

3. **Resource Organization**:
   - GCP uses Labels (similar to Azure Tags)
   - Azure Resource Groups are more flexible than GCP's strictly hierarchical model
   - Azure Management Groups provide policy inheritance not available in GCP

### Azure FinOps Best Practices

1. **Tagging Strategy**:
   - Implement a comprehensive tagging policy
   - Include tags for: Environment, Business Unit, Cost Center, Project, Owner
   - Enforce tags using Azure Policy
   - Use tag inheritance where possible

2. **Subscription Structure**:
   - Design subscriptions around departments or applications
   - Use management groups to organize subscriptions
   - Implement different subscriptions for production vs. non-production

3. **Governance Controls**:
   - Set budgets and alerts at multiple levels
   - Use Azure Policy to enforce allowed resources and regions
   - Implement Blueprints for consistent environments
   - Regular review of Azure Advisor recommendations

4. **Cost Optimization Techniques**:
   - Right-sizing VMs using Azure Advisor
   - Implementing auto-shutdown for dev/test resources
   - Utilizing Azure Spot Instances for interruptible workloads
   - Leverage Azure Hybrid Benefit for Windows and SQL workloads
   - Implementing appropriate storage tiers

5. **Reporting and Analysis**:
   - Schedule regular exports to Azure Storage
   - Implement Power BI dashboards with Cost Management data
   - Create custom views for different stakeholders
   - Analyze anomalies and trends regularly

### Additional Notes on Azure Cost Data

1. **Amortized Costs**:
   - Azure shows both actual and amortized costs for RIs
   - Amortization spreads upfront RI payments across the term

2. **Marketplace Charges**:
   - Third-party services purchased through Azure Marketplace appear as separate line items
   - Often have different billing models than native Azure services

3. **Currencies and Exchange Rates**:
   - Azure may bill in different currencies depending on your agreement
   - Exchange rates are applied at billing time for non-USD transactions

4. **Cost vs. Usage Distinction**:
   - Usage data shows resource consumption
   - Cost data applies pricing to usage
   - Some exports can be usage-only or cost-only
