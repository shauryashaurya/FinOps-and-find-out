# configAzure.py
# Configuration for Azure Billing Data simulation.
# This file defines Azure services, pricing models, example projects,
# and organizational structure to generate realistic billing data for cost analysis and optimization scenarios.

AZURE_REGIONS = [
    "eastus",            # Virginia
    "eastus2",           # Virginia
    "centralus",         # Iowa
    "northcentralus",    # Illinois
    "southcentralus",    # Texas
    "westcentralus",     # Wyoming
    "westus",            # California
    "westus2",           # Washington
    "westus3",           # Arizona
    "canadacentral",     # Toronto
    "canadaeast",        # Quebec
    "brazilsouth",       # Sao Paulo
    "northeurope",       # Ireland
    "westeurope",        # Netherlands
    "uksouth",           # London
    "ukwest",            # Cardiff
    "francecentral",     # Paris
    "francesouth",       # Marseille
    "germanywestcentral",  # Frankfurt
    "germanynorth",      # Berlin
    "norwayeast",        # Oslo
    "norwaywest",        # Stavanger
    "swedencentral",     # Gävle
    "switzerlandnorth",  # Zurich
    "switzerlandwest",   # Geneva
    "eastasia",          # Hong Kong
    "southeastasia",     # Singapore
    "australiaeast",     # New South Wales
    "australiasoutheast",  # Victoria
    "australiacentral",  # Canberra
    "japaneast",         # Tokyo
    "japanwest",         # Osaka
    "koreacentral",      # Seoul
    "koreasouth",        # Busan
    "southindia",        # Chennai
    "centralindia",      # Pune
    "westindia",         # Mumbai
    "southafricanorth",  # Johannesburg
    "southafricawest",   # Cape Town
    "uaenorth",          # Dubai
    "uaecentral"         # Abu Dhabi
]

# Azure availability zones are per region, but most regions have 3 zones
AZURE_AVAILABILITY_ZONES = ["1", "2", "3"]

REGIONAL_COST_FACTORS = {
    "eastus": 1.0,
    "eastus2": 1.0,
    "centralus": 1.0,
    "northcentralus": 1.0,
    "southcentralus": 1.0,
    "westcentralus": 1.05,
    "westus": 1.05,
    "westus2": 1.05,
    "westus3": 1.05,
    "canadacentral": 1.06,
    "canadaeast": 1.06,
    "brazilsouth": 1.14,
    "northeurope": 1.05,
    "westeurope": 1.09,
    "uksouth": 1.1,
    "ukwest": 1.1,
    "francecentral": 1.1,
    "francesouth": 1.12,
    "germanywestcentral": 1.09,
    "germanynorth": 1.1,
    "norwayeast": 1.08,
    "norwaywest": 1.09,
    "swedencentral": 1.06,
    "switzerlandnorth": 1.1,
    "switzerlandwest": 1.1,
    "eastasia": 1.09,
    "southeastasia": 1.07,
    "australiaeast": 1.14,
    "australiasoutheast": 1.14,
    "australiacentral": 1.15,
    "japaneast": 1.12,
    "japanwest": 1.12,
    "koreacentral": 1.13,
    "koreasouth": 1.13,
    "southindia": 1.07,
    "centralindia": 1.07,
    "westindia": 1.08,
    "southafricanorth": 1.15,
    "southafricawest": 1.16,
    "uaenorth": 1.09,
    "uaecentral": 1.09
}

# Azure Services with pricing information
AZURE_SERVICES = {
    "Compute": {
        "VirtualMachines": {
            "base_rate": 0.05,
            "vm_sizes": [
                "Standard_B1ms", "Standard_B2ms", "Standard_B4ms", "Standard_B8ms",
                "Standard_D2s_v3", "Standard_D4s_v3", "Standard_D8s_v3",
                "Standard_E2s_v3", "Standard_E4s_v3", "Standard_E8s_v3",
                "Standard_F2s_v2", "Standard_F4s_v2", "Standard_F8s_v2",
                "Standard_NC6s_v3", "Standard_NC12s_v3"
            ],
            "operations": ["Compute Hours", "OS Licenses", "IP Addresses"],
            "price_range": (0.01, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["ComputeHours", "Storage", "Network"],
            "meter_name_pattern": "Virtual Machines {operation} in {region}",
            "meter_ids": ["F3DB-E132-6157", "D9CA-F45E-1A91", "A5C7-B8E9-3D02"],
        },
        "AKS": {
            "base_rate": 0.10,
            "operations": ["ClusterManagement", "NodePool"],
            "price_range": (0.10, 0.15),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["ClusterManagement", "NodeUsage"],
            "meter_name_pattern": "AKS {operation} in {region}",
            "meter_ids": ["G7A8-H9B1-5C63", "D4E2-F3G5-7H89"],
        },
        "AppService": {
            "base_rate": 0.05,
            "operations": ["Instances", "Storage", "SSL Connections"],
            "price_range": (0.01, 0.20),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["Instances", "Storage", "Network"],
            "meter_name_pattern": "App Service {operation} in {region}",
            "meter_ids": ["C8D9-E1F2-753G", "B7A6-C8D9-E1F2"],
        },
        "Functions": {
            "base_rate": 0.0000025,
            "operations": ["Executions", "Compute", "Network"],
            "price_range": (0.0000020, 0.0000040),
            "pricing_model": "consumption",
            "unit": "Million Executions",
            "usage_types": ["Execution", "GBs", "Network"],
            "meter_name_pattern": "Functions {operation} in {region}",
            "meter_ids": ["H8G7-F6E5-D4C3", "A2B3-C4D5-E6F7"],
        },
        "ContainerInstances": {
            "base_rate": 0.00002,
            "operations": ["vCPU", "Memory", "GPU"],
            "price_range": (0.000016, 0.00003),
            "pricing_model": "consumption",
            "unit": "vCPU-seconds",
            "usage_types": ["CPU", "Memory", "GPU"],
            "meter_name_pattern": "Container Instances {operation} in {region}",
            "meter_ids": ["K9J8-H7G6-F5E4", "L1K2-J3H4-G5F6"],
        },
    },
    "Storage": {
        "BlobStorage": {
            "base_rate": 0.02,
            "operations": ["Hot", "Cool", "Archive", "Read", "Write", "Data Retrieval"],
            "price_range": (0.001, 0.1),
            "pricing_model": "usage",
            "unit": "GB-Month",
            "usage_types": ["StorageHot", "StorageCool", "StorageArchive", "DataRetrieval", "Operations"],
            "meter_name_pattern": "Blob Storage {operation} in {region}",
            "meter_ids": ["M3N4-P5Q6-R7S8", "T9U1-V2W3-X4Y5", "Z6A7-B8C9-D1E2"],
        },
        "ManagedDisks": {
            "base_rate": 0.04,
            "operations": ["Standard HDD", "Standard SSD", "Premium SSD", "Ultra Disk", "Snapshots"],
            "price_range": (0.03, 0.17),
            "pricing_model": "usage",
            "unit": "GB-Month",
            "usage_types": ["StandardHDD", "StandardSSD", "PremiumSSD", "UltraDisk", "Snapshot"],
            "meter_name_pattern": "Managed Disks {operation} in {region}",
            "meter_ids": ["F2E3-D4C5-B6A7", "G8H9-I1J2-K3L4", "M5N6-O7P8-Q9R1"],
        },
        "Files": {
            "base_rate": 0.16,
            "operations": ["Standard", "Premium", "Transactions", "Snapshots"],
            "price_range": (0.13, 0.30),
            "pricing_model": "usage",
            "unit": "GB-Month",
            "usage_types": ["Standard", "Premium", "Transactions"],
            "meter_name_pattern": "Azure Files {operation} in {region}",
            "meter_ids": ["S2T3-U4V5-W6X7", "Y8Z9-A1B2-C3D4"],
        },
    },
    "Database": {
        "SQLDatabase": {
            "base_rate": 0.0364,
            "operations": ["DTU", "vCore", "Storage", "Backup", "HA"],
            "price_range": (0.03, 1.2),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["DTU", "vCore", "Storage", "Backup", "Network"],
            "meter_name_pattern": "SQL Database {operation} in {region}",
            "meter_ids": ["E5F6-G7H8-I9J1", "K2L3-M4N5-O6P7", "Q8R9-S1T2-U3V4"],
        },
        "CosmosDB": {
            "base_rate": 0.90,
            "operations": ["RUs", "Storage", "Backup", "Analytical Storage"],
            "price_range": (0.30, 1.5),
            "pricing_model": "on_demand",
            "unit": "RU/s-Hour",
            "usage_types": ["RUs", "Storage", "Backup", "Analytical"],
            "meter_name_pattern": "Cosmos DB {operation} in {region}",
            "meter_ids": ["W5X6-Y7Z8-A9B1", "C2D3-E4F5-G6H7"],
        },
        "TableStorage": {
            "base_rate": 0.18,
            "operations": ["Storage", "Batch Transactions", "Operations", "Network"],
            "price_range": (0.10, 0.30),
            "pricing_model": "usage",
            "unit": "GB-Month",
            "usage_types": ["Storage", "Transactions", "Operations", "Network"],
            "meter_name_pattern": "Table Storage {operation} in {region}",
            "meter_ids": ["I8J9-K1L2-M3N4", "O5P6-Q7R8-S9T1"],
        },
        "Redis": {
            "base_rate": 0.049,
            "operations": ["Basic", "Standard", "Premium", "Enterprise"],
            "price_range": (0.025, 0.35),
            "pricing_model": "on_demand",
            "unit": "GB-Hour",
            "usage_types": ["InstanceHours", "Network"],
            "meter_name_pattern": "Azure Cache for Redis {operation} in {region}",
            "meter_ids": ["U2V3-W4X5-Y6Z7", "A8B9-C1D2-E3F4"],
        },
    },
    "Analytics": {
        "SynapseAnalytics": {
            "base_rate": 0.02,
            "operations": ["DWU", "Storage", "Serverless", "Spark Pool"],
            "price_range": (0.01, 0.05),
            "pricing_model": "usage",
            "unit": "DWU-Hour",
            "usage_types": ["DWU", "Storage", "Serverless", "Spark"],
            "meter_name_pattern": "Synapse Analytics {operation} in {region}",
            "meter_ids": ["G5H6-I7J8-K9L1", "M2N3-O4P5-Q6R7", "S8T9-U1V2-W3X4"],
        },
        "DataFactory": {
            "base_rate": 0.06,
            "operations": ["Pipeline", "Activity Run", "Data Movement", "Integration Runtime"],
            "price_range": (0.03, 0.09),
            "pricing_model": "usage",
            "unit": "Activity-runs",
            "usage_types": ["Pipeline", "Activity", "DataMovement", "IR"],
            "meter_name_pattern": "Data Factory {operation} in {region}",
            "meter_ids": ["Y5Z6-A7B8-C9D1", "E2F3-G4H5-I6J7"],
        },
        "HDInsight": {
            "base_rate": 0.01,
            "operations": ["Standard", "Premium", "Enterprise", "Compute", "Storage"],
            "price_range": (0.005, 0.03),
            "pricing_model": "on_demand",
            "unit": "vCPU-Hour",
            "usage_types": ["StandardNode", "PremiumNode", "EnterpriseNode"],
            "meter_name_pattern": "HDInsight {operation} in {region}",
            "meter_ids": ["K8L9-M1N2-O3P4", "Q5R6-S7T8-U9V1"],
        },
        "EventHubs": {
            "base_rate": 0.04,
            "operations": ["Basic", "Standard", "Premium", "Throughput Units", "Capture"],
            "price_range": (0.02, 0.06),
            "pricing_model": "usage",
            "unit": "TU-Hour",
            "usage_types": ["Basic", "Standard", "Premium", "Capture"],
            "meter_name_pattern": "Event Hubs {operation} in {region}",
            "meter_ids": ["W2X3-Y4Z5-A6B7", "C8D9-E1F2-G3H4"],
        },
        "ServiceBus": {
            "base_rate": 0.04,
            "operations": ["Basic", "Standard", "Premium", "Operations"],
            "price_range": (0.02, 0.06),
            "pricing_model": "usage",
            "unit": "Message Operations",
            "usage_types": ["Basic", "Standard", "Premium", "Operations"],
            "meter_name_pattern": "Service Bus {operation} in {region}",
            "meter_ids": ["I5J6-K7L8-M9N1", "O2P3-Q4R5-S6T7"],
        },
        "Stream Analytics": {
            "base_rate": 0.08,
            "operations": ["Streaming Units", "Standard", "Job"],
            "price_range": (0.04, 0.12),
            "pricing_model": "usage",
            "unit": "SU-Hour",
            "usage_types": ["StreamingUnits", "Standard"],
            "meter_name_pattern": "Stream Analytics {operation} in {region}",
            "meter_ids": ["U8V9-W1X2-Y3Z4", "A5B6-C7D8-E9F1"],
        },
    },
    "Networking": {
        "VPNGateway": {
            "base_rate": 0.05,
            "operations": ["Basic", "VpnGw1", "VpnGw2", "VpnGw3", "VpnGw4", "VpnGw5"],
            "price_range": (0.03, 0.075),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["GatewayHours", "DataTransfer"],
            "meter_name_pattern": "VPN Gateway {operation} in {region}",
            "meter_ids": ["G2H3-I4J5-K6L7", "M8N9-O1P2-Q3R4"],
        },
        "ExpressRoute": {
            "base_rate": 0.042,
            "operations": ["Metered", "Unlimited", "Premium", "Direct", "Global Reach"],
            "price_range": (0.03, 0.06),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["CircuitHours", "DataTransfer"],
            "meter_name_pattern": "ExpressRoute {operation} in {region}",
            "meter_ids": ["S4T5-U6V7-W8X9", "Y1Z2-A3B4-C5D6"],
        },
        "NATGateway": {
            "base_rate": 0.044,
            "operations": ["Gateway", "Traffic", "Public IP"],
            "price_range": (0.03, 0.06),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["GatewayHour", "DataProcessed"],
            "meter_name_pattern": "NAT Gateway {operation} in {region}",
            "meter_ids": ["E7F8-G9H1-I2J3", "K4L5-M6N7-O8P9"],
        },
        "LoadBalancer": {
            "base_rate": 0.025,
            "operations": ["Basic", "Standard", "Rules", "Outbound Rules"],
            "price_range": (0.01, 0.04),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["LBHours", "DataProcessed"],
            "meter_name_pattern": "Load Balancer {operation} in {region}",
            "meter_ids": ["Q1R2-S3T4-U5V6", "W7X8-Y9Z1-A2B3"],
        },
        "CDN": {
            "base_rate": 0.075,
            "operations": ["Standard", "Premium", "Data Transfer", "Rules"],
            "price_range": (0.04, 0.10),
            "pricing_model": "usage",
            "unit": "GB",
            "usage_types": ["StandardDataTransfer", "PremiumDataTransfer", "Rules"],
            "meter_name_pattern": "CDN {operation} in {region}",
            "meter_ids": ["C4D5-E6F7-G8H9", "I1J2-K3L4-M5N6"],
        },
        "VirtualNetwork": {
            "base_rate": 0.01,
            "operations": ["IP Addresses", "Peering", "Endpoints", "NAT Gateway"],
            "price_range": (0.005, 0.1),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["IPAddresses", "Peering", "Endpoints", "NATGateway"],
            "meter_name_pattern": "Virtual Network {operation} in {region}",
            "meter_ids": ["O6P7-Q8R9-S1T2", "U3V4-W5X6-Y7Z8"],
        },
        "DNSZones": {
            "base_rate": 0.5,
            "operations": ["Public Zones", "Records", "Queries", "Private Zones"],
            "price_range": (0.1, 2.0),
            "pricing_model": "on_demand",
            "unit": "Month",
            "usage_types": ["PublicZones", "PrivateZones", "Queries"],
            "meter_name_pattern": "DNS Zones {operation} in {region}",
            "meter_ids": ["A9B1-C2D3-E4F5", "G6H7-I8J9-K1L2"],
        },
        "DDoSProtection": {
            "base_rate": 5.0,
            "operations": ["Basic", "Standard", "Protected Resources"],
            "price_range": (1.0, 10.0),
            "pricing_model": "on_demand",
            "unit": "Month",
            "usage_types": ["BasicProtection", "StandardProtection", "Resources"],
            "meter_name_pattern": "DDoS Protection {operation} in {region}",
            "meter_ids": ["M2N3-O4P5-Q6R7", "S8T9-U1V2-W3X4"],
        },
        "FrontDoor": {
            "base_rate": 0.025,
            "operations": ["Standard", "Premium", "Routing Rules", "Data Transfer"],
            "price_range": (0.01, 0.05),
            "pricing_model": "usage",
            "unit": "GB",
            "usage_types": ["StandardRouting", "PremiumRouting", "DataTransfer"],
            "meter_name_pattern": "Front Door {operation} in {region}",
            "meter_ids": ["Y4Z5-A6B7-C8D9", "E1F2-G3H4-I5J6"],
        },
    },
    "MachineLearning": {
        "MachineLearning": {
            "base_rate": 0.28,
            "operations": ["Compute", "Managed Endpoints", "Workspaces", "Data Labeling"],
            "price_range": (0.15, 0.50),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["ComputeNodeHours", "EndpointHours", "WorkspaceHours"],
            "meter_name_pattern": "Machine Learning {operation} in {region}",
            "meter_ids": ["K7L8-M9N1-O2P3", "Q4R5-S6T7-U8V9"],
        },
        "OpenAI": {
            "base_rate": 0.0008,
            "operations": ["GPT-3", "GPT-4", "Embeddings", "DALL-E", "Whisper"],
            "price_range": (0.0003, 0.0015),
            "pricing_model": "usage",
            "unit": "1000 Tokens",
            "usage_types": ["TextGeneration", "Embeddings", "ImageGeneration"],
            "meter_name_pattern": "OpenAI {operation} in {region}",
            "meter_ids": ["W1X2-Y3Z4-A5B6", "C7D8-E9F1-G2H3"],
        },
        "CognitiveServices": {
            "base_rate": 0.006,
            "operations": ["Speech", "Vision", "Language", "Decision"],
            "price_range": (0.004, 0.009),
            "pricing_model": "usage",
            "unit": "1000 API Calls",
            "usage_types": ["SpeechRecognition", "ComputerVision", "TextAnalytics"],
            "meter_name_pattern": "Cognitive Services {operation} in {region}",
            "meter_ids": ["I4J5-K6L7-M8N9", "O1P2-Q3R4-S5T6"],
        },
        "BotService": {
            "base_rate": 0.002,
            "operations": ["Standard", "Premium", "Channels", "Transcripts"],
            "price_range": (0.001, 0.004),
            "pricing_model": "usage",
            "unit": "1000 Messages",
            "usage_types": ["StandardMessages", "PremiumMessages", "ChannelUsage"],
            "meter_name_pattern": "Bot Service {operation} in {region}",
            "meter_ids": ["U6V7-W8X9-Y1Z2", "A3B4-C5D6-E7F8"],
        },
    },
    "Management": {
        "Monitor": {
            "base_rate": 0.258,
            "operations": ["Logs", "Metrics", "Alerts", "Application Insights"],
            "price_range": (0.20, 0.30),
            "pricing_model": "usage",
            "unit": "GB",
            "usage_types": ["LogsIngestion", "MetricsStorage", "Alerts", "AppInsights"],
            "meter_name_pattern": "Monitor {operation} in {region}",
            "meter_ids": ["G9H1-I2J3-K4L5", "M6N7-O8P9-Q1R2"],
        },
        "LogAnalytics": {
            "base_rate": 0.50,
            "operations": ["Data Ingestion", "Data Retention", "Sentinel", "Queries"],
            "price_range": (0.30, 0.70),
            "pricing_model": "usage",
            "unit": "GB",
            "usage_types": ["DataIngestion", "DataRetention", "Sentinel", "Queries"],
            "meter_name_pattern": "Log Analytics {operation} in {region}",
            "meter_ids": ["S3T4-U5V6-W7X8", "Y9Z1-A2B3-C4D5"],
        },
        "ApplicationInsights": {
            "base_rate": 0.20,
            "operations": ["Data Collection", "Data Retention", "Availability Tests"],
            "price_range": (0.15, 0.30),
            "pricing_model": "usage",
            "unit": "GB",
            "usage_types": ["DataCollection", "DataRetention", "AvailabilityTests"],
            "meter_name_pattern": "Application Insights {operation} in {region}",
            "meter_ids": ["E6F7-G8H9-I1J2", "K3L4-M5N6-O7P8"],
        },
        "CostManagement": {
            "base_rate": 0.01,
            "operations": ["Exports", "Reports", "Budgets"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "Report",
            "usage_types": ["CostExports", "CostReports", "Budgets"],
            "meter_name_pattern": "Cost Management {operation}",
            "meter_ids": ["Q9R1-S2T3-U4V5", "W6X7-Y8Z9-A1B2"],
        },
        "ManagedGrafana": {
            "base_rate": 9.0,
            "operations": ["Essentials", "Standard", "Enterprise"],
            "price_range": (5.0, 15.0),
            "pricing_model": "monthly",
            "unit": "User-Month",
            "usage_types": ["EssentialsUsers", "StandardUsers", "EnterpriseUsers"],
            "meter_name_pattern": "Managed Grafana {operation} in {region}",
            "meter_ids": ["C2D3-E4F5-G6H7", "I8J9-K1L2-M3N4"],
        },
    },
    "Security": {
        "DefenderForCloud": {
            "base_rate": 0.10,
            "operations": ["Essentials", "Standard", "Server Protection", "Container Protection"],
            "price_range": (0.05, 0.20),
            "pricing_model": "monthly",
            "unit": "Node-Month",
            "usage_types": ["EssentialsAssets", "StandardAssets", "ServerProtection"],
            "meter_name_pattern": "Defender for Cloud {operation} in {region}",
            "meter_ids": ["O4P5-Q6R7-S8T9", "U1V2-W3X4-Y5Z6"],
        },
        "KeyVault": {
            "base_rate": 0.06,
            "operations": ["Operations", "Standard", "Premium", "HSM", "Certificates"],
            "price_range": (0.03, 0.10),
            "pricing_model": "monthly",
            "unit": "Operation",
            "usage_types": ["StandardOperations", "PremiumOperations", "HSMOperations"],
            "meter_name_pattern": "Key Vault {operation} in {region}",
            "meter_ids": ["A7B8-C9D1-E2F3", "G4H5-I6J7-K8L9"],
        },
        "ActiveDirectory": {
            "base_rate": 0.05,
            "operations": ["Free", "P1", "P2", "B2B", "B2C"],
            "price_range": (0.03, 0.08),
            "pricing_model": "monthly",
            "unit": "User-Month",
            "usage_types": ["P1Users", "P2Users", "B2BUsers", "B2CAuthentications"],
            "meter_name_pattern": "Active Directory {operation} in {region}",
            "meter_ids": ["M1N2-O3P4-Q5R6", "S7T8-U9V1-W2X3"],
        },
        "DedicatedHSM": {
            "base_rate": 1.45,
            "operations": ["StandardB1", "High Performance", "Management"],
            "price_range": (1.20, 2.0),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["HSMInstanceHours", "HSMManagement"],
            "meter_name_pattern": "Dedicated HSM {operation} in {region}",
            "meter_ids": ["Y4Z5-A6B7-C8D9", "E1F2-G3H4-I5J6"],
        },
    },
    "Data": {
        "ElasticSearch": {
            "base_rate": 0.10,
            "operations": ["Standard", "Basic", "Enterprise"],
            "price_range": (0.05, 2.0),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["StandardHours", "EnterpriseHours", "Storage"],
            "meter_name_pattern": "Elastic {operation} in {region}",
            "meter_ids": ["J7K8-L9M1-N2O3", "P4Q5-R6S7-T8U9"],
        },
        "PowerBI": {
            "base_rate": 12.0,
            "operations": ["Pro", "Premium", "Embedded", "Capacity"],
            "price_range": (5.0, 25.0),
            "pricing_model": "monthly",
            "unit": "Month",
            "usage_types": ["ProUsers", "PremiumUsers", "EmbeddedCapacity"],
            "meter_name_pattern": "Power BI {operation} in {region}",
            "meter_ids": ["V1W2-X3Y4-Z5A6", "B7C8-D9E1-F2G3"],
        },
    },
    "Healthcare": {
        "HealthDataServices": {
            "base_rate": 0.01,
            "operations": ["FHIR", "DICOM", "IoT Connector", "Storage"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": ["FHIRRequests", "DICOMStorage", "IoTConnections"],
            "meter_name_pattern": "Health Data Services {operation} in {region}",
            "meter_ids": ["H4I5-J6K7-L8M9", "N1O2-P3Q4-R5S6"],
        },
    },
    "Media": {
        "MediaServices": {
            "base_rate": 0.0075,
            "operations": ["Encoding", "Live Events", "Streaming", "Content Protection"],
            "price_range": (0.005, 0.015),
            "pricing_model": "on_demand",
            "unit": "Minute",
            "usage_types": ["EncodingMinutes", "LiveEventHours", "StreamingUnits"],
            "meter_name_pattern": "Media Services {operation} in {region}",
            "meter_ids": ["T7U8-V9W1-X2Y3", "Z4A5-B6C7-D8E9"],
        },
        "VideoIndexer": {
            "base_rate": 0.04,
            "operations": ["Indexing", "Streaming", "Storage"],
            "price_range": (0.02, 0.08),
            "pricing_model": "on_demand",
            "unit": "Minute",
            "usage_types": ["IndexingMinutes", "StreamingMinutes", "Storage"],
            "meter_name_pattern": "Video Indexer {operation} in {region}",
            "meter_ids": ["F1G2-H3I4-J5K6", "L7M8-N9O1-P2Q3"],
        },
        "LiveVideo": {
            "base_rate": 0.2813,
            "operations": ["Live Video Analytics", "Edge Processing", "Cloud Processing"],
            "price_range": (0.15, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hour",
            "usage_types": ["LiveVideoHours", "EdgeProcessingHours", "CloudProcessingHours"],
            "meter_name_pattern": "Live Video {operation} in {region}",
            "meter_ids": ["R3S4-T5U6-V7W8", "X9Y1-Z2A3-B4C5"],
        },
    },
    "Location": {
        "Maps": {
            "base_rate": 0.04,
            "operations": ["Rendering", "Routing", "Search", "Traffic", "Spatial Operations"],
            "price_range": (0.02, 0.08),
            "pricing_model": "on_demand",
            "unit": "1000 Transactions",
            "usage_types": ["Rendering", "Routing", "Search", "SpatialOperations"],
            "meter_name_pattern": "Maps {operation} in {region}",
            "meter_ids": ["D5E6-F7G8-H9I1", "J2K3-L4M5-N6O7"],
        },
    },
    "ApplicationServices": {
        "ArcEnabledServers": {
            "base_rate": 0.10,
            "operations": ["Server", "Kubernetes", "Data Services"],
            "price_range": (0.05, 0.20),
            "pricing_model": "monthly",
            "unit": "Core",
            "usage_types": ["ServerCores", "KubernetesCores", "DataServicesCores"],
            "meter_name_pattern": "Arc Enabled Servers {operation} in {region}",
            "meter_ids": ["P8Q9-R1S2-T3U4", "V5W6-X7Y8-Z9A1"],
        },
        "Logic Apps": {
            "base_rate": 0.40,
            "operations": ["Standard", "Consumption", "Connectors", "Integration Account"],
            "price_range": (0.30, 0.50),
            "pricing_model": "usage",
            "unit": "Action Execution",
            "usage_types": ["StandardActions", "ConsumptionActions", "ConnectorActions"],
            "meter_name_pattern": "Logic Apps {operation} in {region}",
            "meter_ids": ["B2C3-D4E5-F6G7", "H8I9-J1K2-L3M4"],
        },
        "API Management": {
            "base_rate": 0.10,
            "operations": ["Basic", "Standard", "Premium", "Consumption"],
            "price_range": (0.05, 0.20),
            "pricing_model": "hourly",
            "unit": "Hour",
            "usage_types": ["BasicHours", "StandardHours", "PremiumHours", "ConsumptionCalls"],
            "meter_name_pattern": "API Management {operation} in {region}",
            "meter_ids": ["N5O6-P7Q8-R9S1", "T2U3-V4W5-X6Y7"],
        },
        "Service Fabric": {
            "base_rate": 0.012,
            "operations": ["Node Type", "Managed", "Stateless", "Stateful"],
            "price_range": (0.01, 0.02),
            "pricing_model": "hourly",
            "unit": "Core-Hour",
            "usage_types": ["NodeHours", "ManagedClusterHours"],
            "meter_name_pattern": "Service Fabric {operation} in {region}",
            "meter_ids": ["Z8A9-B1C2-D3E4", "F5G6-H7I8-J9K1"],
        },
        "App Configuration": {
            "base_rate": 3.5,
            "operations": ["Standard", "Free", "Operations"],
            "price_range": (1.0, 5.0),
            "pricing_model": "on_demand",
            "unit": "Operation",
            "usage_types": ["StandardOperations", "FreeOperations"],
            "meter_name_pattern": "App Configuration {operation} in {region}",
            "meter_ids": ["L2M3-N4O5-P6Q7", "R8S9-T1U2-V3W4"],
        },
        "Batch": {
            # Free service (pay only for underlying resources)
            "base_rate": 0.0,
            "operations": ["Virtual Machine", "Low Priority VM", "Job Schedule"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Hour",
            "usage_types": ["VMHours", "LowPriorityVMHours", "JobScheduling"],
            "meter_name_pattern": "Batch {operation} in {region}",
            "meter_ids": ["X5Y6-Z7A8-B9C1", "D2E3-F4G5-H6I7"],
        },
    },
    "DevOps": {
        "DevOps": {
            "base_rate": 0.005,
            "operations": ["Pipelines", "Test Plans", "Artifacts", "Self-hosted Pipelines"],
            "price_range": (0.001, 0.01),
            "pricing_model": "on_demand",
            "unit": "Pipeline Run",
            "usage_types": ["PipelineMinutes", "TestPlans", "ArtifactStorage"],
            "meter_name_pattern": "DevOps {operation} in {region}",
            "meter_ids": ["J8K9-L1M2-N3O4", "P5Q6-R7S8-T9U1"],
        },
        "ARM": {
            "base_rate": 0.0,  # Free service
            "operations": ["Template Deployments", "Resource Operations"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Operation",
            "usage_types": ["TemplateDeployments", "ResourceOperations"],
            "meter_name_pattern": "ARM {operation} in {region}",
            "meter_ids": ["V2W3-X4Y5-Z6A7", "B8C9-D1E2-F3G4"],
        },
    },
    "IoT": {
        "IoTHub": {
            "base_rate": 0.08,
            "operations": ["Free", "Basic", "Standard", "Messages", "Device Provisioning"],
            "price_range": (0.05, 0.15),
            "pricing_model": "on_demand",
            "unit": "Million Messages",
            "usage_types": ["FreeMessages", "BasicMessages", "StandardMessages", "DeviceProvisioning"],
            "meter_name_pattern": "IoT Hub {operation} in {region}",
            "meter_ids": ["H5I6-J7K8-L9M1", "N2O3-P4Q5-R6S7"],
        },
        "IoTCentral": {
            "base_rate": 0.10,
            "operations": ["Standard", "Premium", "Devices", "Messages"],
            "price_range": (0.05, 0.20),
            "pricing_model": "on_demand",
            "unit": "Device",
            "usage_types": ["StandardDevices", "PremiumDevices", "Messages"],
            "meter_name_pattern": "IoT Central {operation} in {region}",
            "meter_ids": ["T8U9-V1W2-X3Y4", "Z5A6-B7C8-D9E1"],
        },
        "IoTEdge": {
            "base_rate": 0.25,
            "operations": ["Modules", "Messages", "Storage"],
            "price_range": (0.10, 0.50),
            "pricing_model": "on_demand",
            "unit": "Device-Hour",
            "usage_types": ["ModuleHours", "Messages", "Storage"],
            "meter_name_pattern": "IoT Edge {operation} in {region}",
            "meter_ids": ["F2G3-H4I5-J6K7", "L8M9-N1O2-P3Q4"],
        },
    },
}

USE_CASE_SCENARIOS = [
    "Enterprise Applications",
    "Mobile Applications",
    "Monitoring, Logging and Observability",
    "Enterprise Integration",
    "Data Processing and ETL",
    "Machine Learning and AI",
    "Audit, Security and Compliance",
    "Generative AI and LLMs",
]

# Azure's organizational structure is based on Management Groups -> Subscriptions -> Resource Groups -> Resources
ORGANIZATION_STRUCTURE = {
    "Management Group": {
        "name": "example-organization",
        "id": "mg-12345678-90ab-cdef-1234-567890abcdef",
        "management_groups": {
            "Core": {
                "id": "mg-98765432-10fe-dcba-9876-543210fedcba",
                "subscriptions": {
                    "Security": {
                        "subscription_id": "00000000-0000-0000-0000-000000555555",
                        "subscription_name": "Security Subscription"
                    },
                    "SharedServices": {
                        "subscription_id": "00000000-0000-0000-0000-000000666666",
                        "subscription_name": "Shared Services Subscription"
                    },
                    "Compliance": {
                        "subscription_id": "00000000-0000-0000-0000-000000777777",
                        "subscription_name": "Compliance Subscription"
                    }
                }
            },
            "BusinessUnits": {
                "id": "mg-87654321-098f-edcb-a987-654321fedcba",
                "management_groups": {
                    "Aviation": {
                        "id": "mg-76543210-987f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "Aviation-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200001",
                                "subscription_name": "Aviation Development"
                            },
                            "Aviation-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300001",
                                "subscription_name": "Aviation Staging"
                            },
                            "Aviation-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400001",
                                "subscription_name": "Aviation Production"
                            },
                            "Aviation-Analytics": {
                                "subscription_id": "00000000-0000-0000-0000-000888800001",
                                "subscription_name": "Aviation Analytics"
                            },
                            "Aviation-IoT": {
                                "subscription_id": "00000000-0000-0000-0000-000999900001",
                                "subscription_name": "Aviation IoT"
                            }
                        }
                    },
                    "Pharma": {
                        "id": "mg-65432109-876f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "Pharma-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200002",
                                "subscription_name": "Pharma Development"
                            },
                            "Pharma-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300002",
                                "subscription_name": "Pharma Staging"
                            },
                            "Pharma-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400002",
                                "subscription_name": "Pharma Production"
                            },
                            "Pharma-Research": {
                                "subscription_id": "00000000-0000-0000-0000-000888800002",
                                "subscription_name": "Pharma Research"
                            },
                            "Pharma-Logistics": {
                                "subscription_id": "00000000-0000-0000-0000-000999900002",
                                "subscription_name": "Pharma Logistics"
                            }
                        }
                    },
                    "Manufacturing": {
                        "id": "mg-54321098-765f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "Manufacturing-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200003",
                                "subscription_name": "Manufacturing Development"
                            },
                            "Manufacturing-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300003",
                                "subscription_name": "Manufacturing Staging"
                            },
                            "Manufacturing-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400003",
                                "subscription_name": "Manufacturing Production"
                            },
                            "Manufacturing-IoT": {
                                "subscription_id": "00000000-0000-0000-0000-000888800003",
                                "subscription_name": "Manufacturing IoT"
                            },
                            "Manufacturing-Logistics": {
                                "subscription_id": "00000000-0000-0000-0000-000999900003",
                                "subscription_name": "Manufacturing Logistics"
                            }
                        }
                    },
                    "SupplyChain": {
                        "id": "mg-43210987-654f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "SupplyChain-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200004",
                                "subscription_name": "SupplyChain Development"
                            },
                            "SupplyChain-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300004",
                                "subscription_name": "SupplyChain Staging"
                            },
                            "SupplyChain-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400004",
                                "subscription_name": "SupplyChain Production"
                            },
                            "SupplyChain-Logistics": {
                                "subscription_id": "00000000-0000-0000-0000-000888800004",
                                "subscription_name": "SupplyChain Logistics"
                            },
                            "SupplyChain-Analytics": {
                                "subscription_id": "00000000-0000-0000-0000-000999900004",
                                "subscription_name": "SupplyChain Analytics"
                            }
                        }
                    },
                    "SoftwareSolutions": {
                        "id": "mg-32109876-543f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "SoftwareSolutions-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200005",
                                "subscription_name": "SoftwareSolutions Development"
                            },
                            "SoftwareSolutions-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300005",
                                "subscription_name": "SoftwareSolutions Staging"
                            },
                            "SoftwareSolutions-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400005",
                                "subscription_name": "SoftwareSolutions Production"
                            },
                            "SoftwareSolutions-CustomerData": {
                                "subscription_id": "00000000-0000-0000-0000-000888800005",
                                "subscription_name": "SoftwareSolutions Customer Data"
                            },
                            "SoftwareSolutions-Analytics": {
                                "subscription_id": "00000000-0000-0000-0000-000999900005",
                                "subscription_name": "SoftwareSolutions Analytics"
                            }
                        }
                    },
                    "MachineLearning": {
                        "id": "mg-21098765-432f-edcb-a987-654321fedcba",
                        "subscriptions": {
                            "ML-Dev": {
                                "subscription_id": "00000000-0000-0000-0000-000222200006",
                                "subscription_name": "Machine Learning Development"
                            },
                            "ML-Staging": {
                                "subscription_id": "00000000-0000-0000-0000-000333300006",
                                "subscription_name": "Machine Learning Staging"
                            },
                            "ML-Prod": {
                                "subscription_id": "00000000-0000-0000-0000-000444400006",
                                "subscription_name": "Machine Learning Production"
                            },
                            "ML-FeatureStore": {
                                "subscription_id": "00000000-0000-0000-0000-000888800006",
                                "subscription_name": "Machine Learning Feature Store"
                            },
                            "ML-Analytics": {
                                "subscription_id": "00000000-0000-0000-0000-000999900006",
                                "subscription_name": "Machine Learning Analytics"
                            }
                        }
                    }
                }
            },
            "Sandbox": {
                "id": "mg-10987654-321f-edcb-a987-654321fedcba",
                "subscriptions": {
                    "Sandbox-Central": {
                        "subscription_id": "00000000-0000-0000-0000-000222299999",
                        "subscription_name": "Sandbox Central"
                    }
                }
            }
        }
    }
}

# Billing accounts
BILLING_ACCOUNTS = {
    "primary": {
        "id": "01A2B3-C4D5E6-F7G8H9",
        "display_name": "Primary Billing Account",
        "open": True,
    },
    "development": {
        "id": "98H7G6-F5E4D3-C2B1A0",
        "display_name": "Development Billing Account",
        "open": True,
    },
    "research": {
        "id": "45K6L7-M8N9P0-Q1R2S3",
        "display_name": "Research Billing Account",
        "open": True,
    }
}

# Create a more comprehensive project-to-billing mapping
SUBSCRIPTION_BILLING_MAPPING = {
    # Development environments use the development billing account
    "00000000-0000-0000-0000-000222200001": "development",
    "00000000-0000-0000-0000-000222200002": "development",
    "00000000-0000-0000-0000-000222200003": "development",
    "00000000-0000-0000-0000-000222200004": "development",
    "00000000-0000-0000-0000-000222200005": "development",
    "00000000-0000-0000-0000-000222200006": "development",
    "00000000-0000-0000-0000-000222299999": "development",

    # Map by subscription display names too
    "Aviation Development": "development",
    "Pharma Development": "development",
    "Manufacturing Development": "development",
    "SupplyChain Development": "development",
    "SoftwareSolutions Development": "development",
    "Machine Learning Development": "development",
    "Sandbox Central": "development",

    # Research projects use the research billing account
    "00000000-0000-0000-0000-000888800002": "research",
    "00000000-0000-0000-0000-000888800006": "research",
    "Pharma Research": "research",
    "Machine Learning Feature Store": "research",

    # By stage patterns
    "dev": "development",
    "sandbox": "development",
    "research": "research",
    "featurestore": "research",

    # All other subscriptions use the primary billing account (default)
}

# Create a direct mapping between stages and subscriptions
STAGE_TO_SUBSCRIPTION_MAPPING = {
    # Aviation
    "aviation-dev": {"subscription_id": "00000000-0000-0000-0000-000222200001", "subscription_name": "Aviation Development"},
    "aviation-staging": {"subscription_id": "00000000-0000-0000-0000-000333300001", "subscription_name": "Aviation Staging"},
    "aviation-prod": {"subscription_id": "00000000-0000-0000-0000-000444400001", "subscription_name": "Aviation Production"},
    "aviation-analytics": {"subscription_id": "00000000-0000-0000-0000-000888800001", "subscription_name": "Aviation Analytics"},
    "aviation-iot": {"subscription_id": "00000000-0000-0000-0000-000999900001", "subscription_name": "Aviation IoT"},

    # Pharma
    "pharma-dev": {"subscription_id": "00000000-0000-0000-0000-000222200002", "subscription_name": "Pharma Development"},
    "pharma-staging": {"subscription_id": "00000000-0000-0000-0000-000333300002", "subscription_name": "Pharma Staging"},
    "pharma-prod": {"subscription_id": "00000000-0000-0000-0000-000444400002", "subscription_name": "Pharma Production"},
    "pharma-research": {"subscription_id": "00000000-0000-0000-0000-000888800002", "subscription_name": "Pharma Research"},
    "pharma-logistics": {"subscription_id": "00000000-0000-0000-0000-000999900002", "subscription_name": "Pharma Logistics"},

    # Manufacturing
    "manufacturing-dev": {"subscription_id": "00000000-0000-0000-0000-000222200003", "subscription_name": "Manufacturing Development"},
    "manufacturing-staging": {"subscription_id": "00000000-0000-0000-0000-000333300003", "subscription_name": "Manufacturing Staging"},
    "manufacturing-prod": {"subscription_id": "00000000-0000-0000-0000-000444400003", "subscription_name": "Manufacturing Production"},
    "manufacturing-iot": {"subscription_id": "00000000-0000-0000-0000-000888800003", "subscription_name": "Manufacturing IoT"},
    "manufacturing-logistics": {"subscription_id": "00000000-0000-0000-0000-000999900003", "subscription_name": "Manufacturing Logistics"},

    # SupplyChain
    "supplychain-dev": {"subscription_id": "00000000-0000-0000-0000-000222200004", "subscription_name": "SupplyChain Development"},
    "supplychain-staging": {"subscription_id": "00000000-0000-0000-0000-000333300004", "subscription_name": "SupplyChain Staging"},
    "supplychain-prod": {"subscription_id": "00000000-0000-0000-0000-000444400004", "subscription_name": "SupplyChain Production"},
    "supplychain-logistics": {"subscription_id": "00000000-0000-0000-0000-000888800004", "subscription_name": "SupplyChain Logistics"},
    "supplychain-analytics": {"subscription_id": "00000000-0000-0000-0000-000999900004", "subscription_name": "SupplyChain Analytics"},

    # SoftwareSolutions
    "softwaresolutions-dev": {"subscription_id": "00000000-0000-0000-0000-000222200005", "subscription_name": "SoftwareSolutions Development"},
    "softwaresolutions-staging": {"subscription_id": "00000000-0000-0000-0000-000333300005", "subscription_name": "SoftwareSolutions Staging"},
    "softwaresolutions-prod": {"subscription_id": "00000000-0000-0000-0000-000444400005", "subscription_name": "SoftwareSolutions Production"},
    "softwaresolutions-customerdata": {"subscription_id": "00000000-0000-0000-0000-000888800005", "subscription_name": "SoftwareSolutions Customer Data"},
    "softwaresolutions-analytics": {"subscription_id": "00000000-0000-0000-0000-000999900005", "subscription_name": "SoftwareSolutions Analytics"},

    # MachineLearning
    "ml-dev": {"subscription_id": "00000000-0000-0000-0000-000222200006", "subscription_name": "Machine Learning Development"},
    "ml-staging": {"subscription_id": "00000000-0000-0000-0000-000333300006", "subscription_name": "Machine Learning Staging"},
    "ml-prod": {"subscription_id": "00000000-0000-0000-0000-000444400006", "subscription_name": "Machine Learning Production"},
    "ml-featurestore": {"subscription_id": "00000000-0000-0000-0000-000888800006", "subscription_name": "Machine Learning Feature Store"},
    "ml-analytics": {"subscription_id": "00000000-0000-0000-0000-000999900006", "subscription_name": "Machine Learning Analytics"},

    # Core Services
    "security": {"subscription_id": "00000000-0000-0000-0000-000000555555", "subscription_name": "Security Subscription"},
    "shared-services": {"subscription_id": "00000000-0000-0000-0000-000000666666", "subscription_name": "Shared Services Subscription"},
    "compliance": {"subscription_id": "00000000-0000-0000-0000-000000777777", "subscription_name": "Compliance Subscription"},
    "sandbox-central": {"subscription_id": "00000000-0000-0000-0000-000222299999", "subscription_name": "Sandbox Central"},
}

PROJECT_LIFECYCLES = [
    "growing",
    "growing_then_sunset",
    "just_started",
    "steady_state",
    "declining",
    "peak_and_plateau",
    "decommissioned"
]

PROJECT_STAGES = [
    "dev",
    "staging",
    "prod",
    "security",
    "shared-services",
    "compliance",
    "analytics",
    "research",
    "iot",
    "logistics",
    "customerdata",
    "featurestore",
    "sandbox",
]

CONFIGURABLES = {
    "number_of_days": 512,
    "annual_budget": 250000000,  # Annual Budget
    "usage_growth_rate": {
        "growing": 1.002,
        "growing_then_sunset": 1.001,
        "just_started": 1.0005,
        "steady_state": 1.00005,  # Minimal steady state growth
        "declining": 0.999,
        "peak_and_plateau": 1.0002,  # Slow growth to plateau
    },
    "sunset_start_day_ratio": 0.6,
    "sunset_decline_rate": 0.997,
    "peak_plateau_start_day_ratio": 0.4,
    "peak_plateau_duration_ratio": 0.4,  # Plateau lasts for 40% of days
}

# Service Mapping from GCP to Azure (for project migration)
GCP_TO_AZURE_SERVICE_MAPPING = {
    # Compute
    "ComputeEngine": "VirtualMachines",
    "GKE": "AKS",
    "CloudRun": "ContainerInstances",
    "AppEngine": "AppService",
    "CloudFunctions": "Functions",

    # Storage
    "CloudStorage": "BlobStorage",
    "PersistentDisk": "ManagedDisks",
    "Filestore": "Files",

    # Database
    "CloudSQL": "SQLDatabase",
    "CloudSpanner": "CosmosDB",
    "Firestore": "CosmosDB",
    "Bigtable": "TableStorage",
    "Memorystore": "Redis",

    # Analytics
    "BigQuery": "SynapseAnalytics",
    "Dataflow": "DataFactory",
    "Dataproc": "HDInsight",
    "Pub/Sub": "EventHubs",
    "Datastream": "DataFactory",

    # Networking
    "CloudVPN": "VPNGateway",
    "CloudInterconnect": "ExpressRoute",
    "CloudNAT": "NATGateway",
    "CloudLoadBalancing": "LoadBalancer",
    "CloudCDN": "CDN",
    "VPC": "VirtualNetwork",
    "CloudDNS": "DNSZones",
    "CloudArmor": "DDoSProtection",

    # Machine Learning
    "VertexAI": "MachineLearning",
    "AIProtagonist": "OpenAI",
    "SpeechToText": "CognitiveServices",
    "DialogFlow": "BotService",

    # Management
    "CloudMonitoring": "Monitor",
    "CloudLogging": "LogAnalytics",
    "CloudTracing": "ApplicationInsights",
    "ErrorReporting": "ApplicationInsights",
    "CloudTrace": "ApplicationInsights",
    "CloudBilling": "CostManagement",
    "ManagedGrafana": "ManagedGrafana",

    # Security
    "SecurityCommandCenter": "DefenderForCloud",
    "SecretManager": "KeyVault",
    "IAM": "ActiveDirectory",
    "KeyManagementService": "KeyVault",
    "CloudHSM": "DedicatedHSM",
    "Certificate Manager": "KeyVault",

    # Data
    "ElasticSearch": "ElasticSearch",
    "Looker": "PowerBI",

    # Healthcare
    "HealthLake": "HealthDataServices",

    # Media
    "MediaConvert": "MediaServices",
    "MediaPackage": "MediaServices",
    "MediaLive": "LiveVideo",
    "MediaConnect": "LiveVideo",
    "Elemental": "MediaServices",

    # Location
    "Location": "Maps",

    # Application Services
    "Anthos": "ArcEnabledServers",
    "CloudTasks": "Logic Apps",
    "CloudScheduler": "Logic Apps",
    "AppMesh": "Service Fabric",
    "ApiGateway": "API Management",
    "BatchService": "Batch",

    # DevOps
    "CloudBuild": "DevOps",
    "DeploymentManager": "ARM",

    # IoT
    "IoT": "IoTHub",
    "IoTSiteWise": "IoTCentral",
    "IoTAnalytics": "IoTEdge",
}

CONFIG = {
    "number_of_days": CONFIGURABLES["number_of_days"],
    "annual_budget": CONFIGURABLES["annual_budget"],
    "services": AZURE_SERVICES,
    "use_case_scenarios": USE_CASE_SCENARIOS,
    "organization_structure": ORGANIZATION_STRUCTURE,
    "billing_accounts": BILLING_ACCOUNTS,
    "subscription_billing_mapping": SUBSCRIPTION_BILLING_MAPPING,
    "STAGE_TO_SUBSCRIPTION_MAPPING": STAGE_TO_SUBSCRIPTION_MAPPING,
    "project_lifecycles": PROJECT_LIFECYCLES,
    "project_stages": PROJECT_STAGES,
    "configurables": CONFIGURABLES,
    "azure_regions": AZURE_REGIONS,
    "azure_availability_zones": AZURE_AVAILABILITY_ZONES,
    "regional_cost_factors": REGIONAL_COST_FACTORS,
    "gcp_to_azure_mapping": GCP_TO_AZURE_SERVICE_MAPPING,
    "projects": {
        # Aviation Business Unit Projects
        "AerodynamicPerformanceAnalysis": {
            "description": "Aircraft aerodynamic performance analysis using cloud-based ETL and analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "HDInsight",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["aviation-analytics"],
            "business_unit": "Aviation",
        },
        "SkyConnectPassengerApp": {
            "description": "Mobile application for airline passengers providing flight information and services.",
            "use_case": "Mobile Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "Functions",
                "CosmosDB",
                "API Management",
                "ActiveDirectory",
                "CDN",
                "EventHubs",
                "LogAnalytics",
                "DDoSProtection",
            ],
            "stages": ["aviation-prod", "aviation-dev"],
            "business_unit": "Aviation",
        },
        "GuardianAirTrafficControl": {
            "description": "Mission-critical air traffic control system ensuring safe and efficient flight operations.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "VirtualNetwork",
                "ExpressRoute",
                "LogAnalytics",
                "DNSZones",
            ],
            "stages": ["aviation-prod", "aviation-staging"],
            "business_unit": "Aviation",
        },
        "RunwayOperationsMonitoring": {
            "description": "Real-time monitoring and analytics of runway conditions and airport operations.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "growing",
            "services": [
                "Monitor",
                "ManagedGrafana",
                "Monitor",
                "LogAnalytics",
                "LogAnalytics",
            ],
            "stages": ["aviation-analytics"],
            "business_unit": "Aviation",
        },
        "JetEngineTelemetryAnalysis": {
            "description": "Advanced analytics of jet engine telemetry data for performance optimization and predictive maintenance.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "SynapseAnalytics",
                "HDInsight",
                "LogAnalytics",
            ],
            "stages": ["aviation-iot", "aviation-analytics"],
            "business_unit": "Aviation",
        },

        # Pharma Business Unit Projects
        "MoleculeSynthesizerAI": {
            "description": "AI-driven platform for synthesizing novel molecules for pharmaceutical research and development.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "growing",
            "services": [
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "VirtualMachines",
                "BlobStorage",
                "DataFactory",
                "CosmosDB",
                "MachineLearning",
                "LogAnalytics",
            ],
            "stages": ["pharma-research", "pharma-staging", "pharma-prod"],
            "business_unit": "Pharma",
        },
        "TrialMasterClinicalPlatform": {
            "description": "Comprehensive platform for managing and executing clinical trials, ensuring compliance and data integrity.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "API Management",
                "ActiveDirectory",
                "LogAnalytics",
                "LogAnalytics",
                "DDoSProtection",
                "EventHubs",
            ],
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "PillProductionQualityControl": {
            "description": "Machine learning system for real-time quality control in pharmaceutical pill production.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "EventHubs",
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "HDInsight",
                "SynapseAnalytics",
                "LogAnalytics",
            ],
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "GenomeAnalyticsWorkbench": {
            "description": "Advanced workbench for genomic data analysis, enabling faster and more accurate research.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "HDInsight",
                "SynapseAnalytics",
                "DataFactory",
                "VirtualMachines",
                "LogAnalytics",
            ],
            "stages": ["pharma-research", "pharma-analytics"],
            "business_unit": "Pharma",
        },
        "PersonalizedDrugRecommendationEngine": {
            "description": "Generative AI engine to provide personalized drug recommendations based on patient profiles.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "just_started",
            "services": [
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "BotService",
                "LogAnalytics",
            ],
            "stages": ["pharma-research"],
            "business_unit": "Pharma",
        },
        "GxPComplianceDashboard": {
            "description": "Dashboard to monitor and ensure GxP compliance across pharmaceutical production and research.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "DefenderForCloud",
                "DefenderForCloud",
                "DefenderForCloud",
                "LogAnalytics",
                "LogAnalytics",
            ],
            "stages": ["pharma-prod", "compliance"],
            "business_unit": "Pharma",
        },
        "MediSupplyChainTracker": {
            "description": "Real-time tracking and visibility platform for the medical supply chain, improving logistics and efficiency.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "EventHubs",
                "EventHubs",
                "CosmosDB",
                "API Management",
                "PowerBI",
                "Functions",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["pharma-logistics"],
            "business_unit": "Pharma",
        },
        "RDExperimentDataPipeline": {
            "description": "Automated data pipeline for managing and processing research and development experiment data.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "DataFactory",
                "Logic Apps",
                "BlobStorage",
                "VirtualMachines",
                "MachineLearning",
                "LogAnalytics",
            ],
            "stages": ["pharma-research"],
            "business_unit": "Pharma",
        },

        # Manufacturing Business Unit Projects
        "SmartFactoryRealTimeData": {
            "description": "Real-time data platform for smart factory operations, collecting and analyzing sensor data from manufacturing equipment.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "PowerBI",
                "HDInsight",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["manufacturing-iot", "manufacturing-analytics", "manufacturing-prod"],
            "business_unit": "Manufacturing",
        },
        "EquipmentPredictiveMaintenance": {
            "description": "Predictive maintenance system using machine learning to forecast equipment failures and optimize maintenance schedules.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "BlobStorage",
                "CosmosDB",
                "EventHubs",
                "PowerBI",
                "LogAnalytics",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging", "manufacturing-analytics"],
            "business_unit": "Manufacturing",
        },
        "ComponentSupplyChainVisibility": {
            "description": "Platform for enhanced visibility and tracking of components across the manufacturing supply chain.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "EventHubs",
                "EventHubs",
                "CosmosDB",
                "API Management",
                "PowerBI",
                "Functions",
                "LogAnalytics",
            ],
            "stages": ["manufacturing-logistics", "manufacturing-prod"],
            "business_unit": "Manufacturing",
        },
        "AutomatedQualityInspection": {
            "description": "Automated visual quality inspection system for manufactured products using AI and computer vision.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "MachineLearning",
                "BlobStorage",
                "Functions",
                "API Management",
                "Logic Apps",
                "LogAnalytics",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging"],
            "business_unit": "Manufacturing",
        },
        "ProductionLineDashboard": {
            "description": "Real-time dashboard providing key performance indicators and operational insights for manufacturing production lines.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "Monitor",
                "LogAnalytics",
                "Monitor",
                "ApplicationInsights",
                "EventHubs",
            ],
            "stages": ["manufacturing-prod", "manufacturing-iot"],
            "business_unit": "Manufacturing",
        },
        "EnterpriseResourcePlanning": {
            "description": "Comprehensive ERP system to manage all aspects of manufacturing operations, from resource planning to financial management.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "VirtualMachines",
                "VirtualNetwork",
                "ExpressRoute",
                "LogAnalytics",
                "LogAnalytics",
                "DNSZones",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging"],
            "business_unit": "Manufacturing",
        },
        "FactoryFloorComplianceSystem": {
            "description": "System to ensure factory floor operations adhere to industry regulations and compliance standards.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "DefenderForCloud",
                "DefenderForCloud",
                "DefenderForCloud",
                "LogAnalytics",
                "LogAnalytics",
            ],
            "stages": ["manufacturing-prod", "compliance"],
            "business_unit": "Manufacturing",
        },

        # Supply Chain Business Unit Projects
        "GlobalShipmentTracker": {
            "description": "Global shipment tracking platform providing end-to-end visibility for all shipments across the supply chain.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "EventHubs",
                "EventHubs",
                "CosmosDB",
                "API Management",
                "PowerBI",
                "Functions",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["supplychain-logistics", "supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "WarehouseManagementApp": {
            "description": "Application for managing warehouse operations, inventory, and order fulfillment.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "VirtualMachines",
                "VirtualNetwork",
                "CDN",
                "DDoSProtection",
                "LogAnalytics",
                "DNSZones",
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "SupplierSelfServicePortal": {
            "description": "Self-service portal for suppliers to manage orders, invoices, and communication with the organization.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "API Management",
                "ActiveDirectory",
                "CDN",
                "DDoSProtection",
                "LogAnalytics",
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "DemandForecastAI": {
            "description": "AI-powered demand forecasting system to predict future demand and optimize inventory levels.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "MachineLearning",
                "MachineLearning",
                "MachineLearning",
                "BlobStorage",
                "DataFactory",
                "SynapseAnalytics",
                "PowerBI",
                "LogAnalytics",
            ],
            "stages": ["supplychain-analytics", "supplychain-staging", "supplychain-prod"],
            "business_unit": "SupplyChain",
        },
        "RouteOptimizationEngine": {
            "description": "Engine for optimizing delivery routes and logistics operations to reduce costs and improve delivery times.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "DataFactory",
                "SynapseAnalytics",
                "HDInsight",
                "SynapseAnalytics",
                "BlobStorage",
                "Logic Apps",
                "LogAnalytics",
            ],
            "stages": ["supplychain-logistics", "supplychain-analytics"],
            "business_unit": "SupplyChain",
        },
        "InventoryVisibilityPlatform": {
            "description": "Platform providing real-time visibility into inventory levels and locations across the entire supply chain network.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "EventHubs",
                "EventHubs",
                "SynapseAnalytics",
                "BlobStorage",
                "PowerBI",
                "Functions",
                "LogAnalytics",
            ],
            "stages": ["supplychain-logistics", "supplychain-prod"],
            "business_unit": "SupplyChain",
        },
        "TradeComplianceMonitor": {
            "description": "System to monitor and ensure compliance with international trade regulations and tariffs.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "DefenderForCloud",
                "DefenderForCloud",
                "DefenderForCloud",
                "LogAnalytics",
                "LogAnalytics",
            ],
            "stages": ["supplychain-prod", "compliance"],
            "business_unit": "SupplyChain",
        },

        # Software Solutions Business Unit Projects
        "CloudAppSaaSBackend": {
            "description": "Backend infrastructure for a SaaS application providing core services and data management.",
            "use_case": "Software Solutions",
            "lifecycle": "growing",
            "services": [
                "VirtualMachines",
                "ContainerInstances",
                "SQLDatabase",
                "CosmosDB",
                "VirtualMachines",
                "API Management",
                "Functions",
                "Redis",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "CustomerServiceHelpCenter": {
            "description": "Online help center and support portal for SaaS customers, offering knowledge base and ticketing system.",
            "use_case": "Software Solutions",
            "lifecycle": "peak_and_plateau",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "API Management",
                "ActiveDirectory",
                "CDN",
                "DDoSProtection",
                "LogAnalytics",
                "DNSZones",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "TeamCollaborationHub": {
            "description": "Enterprise-grade team collaboration and communication platform for internal company use.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "VirtualMachines",
                "SQLDatabase",
                "VirtualMachines",
                "VirtualNetwork",
                "ExpressRoute",
                "LogAnalytics",
                "LogAnalytics",
                "DNSZones",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "SaaSCustomerInsights": {
            "description": "Analytics and business intelligence platform providing insights into SaaS customer usage and behavior.",
            "use_case": "Analytics",
            "lifecycle": "growing",
            "services": [
                "SynapseAnalytics",
                "PowerBI",
                "DataFactory",
                "BlobStorage",
                "SynapseAnalytics",
                "HDInsight",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-customerdata", "softwaresolutions-analytics", "softwaresolutions-prod"],
            "business_unit": "SoftwareSolutions",
        },
        "FeatureRolloutManager": {
            "description": "System to manage and control the rollout of new features to SaaS customers, enabling gradual releases and A/B testing.",
            "use_case": "Software Solutions",
            "lifecycle": "just_started",
            "services": [
                "Functions",
                "CosmosDB",
                "API Management",
                "Logic Apps",
                "EventHubs",
                "EventHubs",
                "EventHubs",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-dev"],
            "business_unit": "SoftwareSolutions",
        },
        "CustomerDataLakehouse": {
            "description": "Scalable data lakehouse for storing and analyzing customer data to improve SaaS offering and customer experience.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "BlobStorage",
                "DataFactory",
                "DataFactory",
                "SynapseAnalytics",
                "HDInsight",
                "SynapseAnalytics",
                "DefenderForCloud",
                "DefenderForCloud",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-customerdata"],
            "business_unit": "SoftwareSolutions",
        },
        "CloudServiceTrustPlatform": {
            "description": "Platform to demonstrate and manage trust and compliance for the SaaS offering, addressing security and regulatory requirements.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "DefenderForCloud",
                "DefenderForCloud",
                "DefenderForCloud",
                "LogAnalytics",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-prod", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "AIHelpdeskChatbot": {
            "description": "AI-powered chatbot to provide automated customer support and answer common helpdesk queries.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "just_started",
            "services": [
                "MachineLearning",
                "BotService",
                "MachineLearning",
                "MachineLearning",
                "Functions",
                "CosmosDB",
                "API Management",
                "LogAnalytics",
            ],
            "stages": ["softwaresolutions-dev"],
            "business_unit": "SoftwareSolutions",
        },
    }
}
