# config.py
# Configuration for Google Cloud Platform (GCP) Billing Data simulation.
# This file defines GCP services, pricing models, example projects,
# and organizational structure to generate realistic billing data for cost analysis and optimization scenarios.

GCP_REGIONS = [
    "us-central1",     # Iowa
    "us-east1",        # South Carolina
    "us-east4",        # Northern Virginia
    "us-west1",        # Oregon
    "us-west2",        # Los Angeles
    "us-west3",        # Salt Lake City
    "us-west4",        # Las Vegas
    "northamerica-northeast1",  # Montreal
    "northamerica-northeast2",  # Toronto
    "southamerica-east1",      # São Paulo
    "europe-west1",    # Belgium
    "europe-west2",    # London
    "europe-west3",    # Frankfurt
    "europe-west4",    # Netherlands
    "europe-west6",    # Zurich
    "europe-central2",  # Warsaw
    "europe-north1",   # Finland
    "asia-east1",      # Taiwan
    "asia-east2",      # Hong Kong
    "asia-northeast1",  # Tokyo
    "asia-northeast2",  # Osaka
    "asia-northeast3",  # Seoul
    "asia-south1",     # Mumbai
    "asia-south2",     # Delhi
    "asia-southeast1",  # Singapore
    "asia-southeast2",  # Jakarta
    "australia-southeast1",    # Sydney
    "australia-southeast2",    # Melbourne
]

# GCP zones follow a pattern of [region]-[a/b/c]
GCP_ZONES = []
for region in GCP_REGIONS:
    for zone_suffix in ['a', 'b', 'c']:
        GCP_ZONES.append(f"{region}-{zone_suffix}")

REGIONAL_COST_FACTORS = {
    "us-central1": 1.0,
    "us-east1": 1.0,
    "us-east4": 1.05,
    "us-west1": 1.0,
    "us-west2": 1.05,
    "us-west3": 1.02,
    "us-west4": 1.02,
    "northamerica-northeast1": 1.06,
    "northamerica-northeast2": 1.06,
    "southamerica-east1": 1.14,
    "europe-west1": 1.05,
    "europe-west2": 1.09,
    "europe-west3": 1.08,
    "europe-west4": 1.07,
    "europe-west6": 1.10,
    "europe-central2": 1.08,
    "europe-north1": 1.06,
    "asia-east1": 1.08,
    "asia-east2": 1.09,
    "asia-northeast1": 1.12,
    "asia-northeast2": 1.12,
    "asia-northeast3": 1.13,
    "asia-south1": 1.07,
    "asia-south2": 1.08,
    "asia-southeast1": 1.09,
    "asia-southeast2": 1.09,
    "australia-southeast1": 1.13,
    "australia-southeast2": 1.14,
}

# GCP Services with pricing information
GCP_SERVICES = {
    "Compute": {
        "ComputeEngine": {
            "base_rate": 0.05,
            "machine_types": [
                "n1-standard-1", "n1-standard-2", "n1-standard-4", "n1-standard-8",
                "n2-standard-2", "n2-standard-4", "n2-standard-8",
                "e2-standard-2", "e2-standard-4", "e2-standard-8",
                "c2-standard-4", "c2-standard-8",
                "n2d-standard-2", "n2d-standard-4", "n2d-standard-8",
            ],
            "operations": ["Instance", "PD-SSD", "PD-HDD", "IP-Address", "GPU"],
            "price_range": (0.01, 5.0),
            "pricing_model": "on_demand",
            "unit": "hour",
            "usage_types": ["Instance", "Storage", "Network"],
            "sku_name_pattern": "Compute Engine {operation} running in {region}",
            "sku_ids": ["8C93-B842-361A", "6C71-E844-38BC", "9D23-58F9-2635"],
        },
        "GKE": {
            "base_rate": 0.10,
            "operations": ["Standard_Cluster", "Autopilot", "NodePool", "Management"],
            "price_range": (0.10, 0.15),
            "pricing_model": "hourly",
            "unit": "hour",
            "usage_types": ["ClusterManagement", "NodeUsage"],
            "sku_name_pattern": "Kubernetes Engine {operation} in {region}",
            "sku_ids": ["F17B-412E-CB64", "4780-C6F3-A836"],
        },
        "CloudRun": {
            "base_rate": 0.00002,
            "operations": ["Requests", "Execution", "CPU", "Memory"],
            "price_range": (0.000016, 0.00003),
            "pricing_model": "consumption",
            "unit": "vCPU-seconds",
            "usage_types": ["CPU", "Memory", "Requests"],
            "sku_name_pattern": "Cloud Run {operation} in {region}",
            "sku_ids": ["42F0-48E2-1869", "F5B0-72E3-86A8"],
        },
        "AppEngine": {
            "base_rate": 0.05,
            "operations": ["Instances", "Backend", "Search", "Datastore"],
            "price_range": (0.01, 0.20),
            "pricing_model": "on_demand",
            "unit": "hour",
            "usage_types": ["Instances", "Storage", "Network"],
            "sku_name_pattern": "App Engine {operation} in {region}",
            "sku_ids": ["B8CA-A13E-778D", "A9FB-B1A3-E645"],
        },
        "CloudFunctions": {
            "base_rate": 0.0000025,
            "operations": ["Invocations", "Compute", "Network"],
            "price_range": (0.0000020, 0.0000040),
            "pricing_model": "consumption",
            "unit": "GHz-second",
            "usage_types": ["Execution", "Invocations", "Network"],
            "sku_name_pattern": "Cloud Functions {operation} in {region}",
            "sku_ids": ["67CD-32B3-F89A", "96E2-2430-C6A2"],
        },
    },
    "Storage": {
        "CloudStorage": {
            "base_rate": 0.02,
            "operations": ["Standard", "Nearline", "Coldline", "Archive", "Read", "Write"],
            "price_range": (0.001, 0.1),
            "pricing_model": "usage",
            "unit": "GiB-month",
            "usage_types": ["StorageStandard", "StorageNearline", "StorageColdline", "StorageArchive", "DataRetrieval", "Operations"],
            "sku_name_pattern": "Cloud Storage {operation} in {region}",
            "sku_ids": ["93E3-4BDC-928A", "7D2D-AB84-E20E", "5E42-2FDC-A1CC"],
        },
        "PersistentDisk": {
            "base_rate": 0.04,
            "operations": ["SSD", "Balanced", "HDD", "Extreme", "Snapshot"],
            "price_range": (0.03, 0.17),
            "pricing_model": "usage",
            "unit": "GiB-month",
            "usage_types": ["SSD", "Balanced", "HDD", "Extreme", "Snapshot"],
            "sku_name_pattern": "Persistent Disk {operation} in {region}",
            "sku_ids": ["E5F2-BBA9-0D14", "1D8A-CF43-68D2", "B6CC-F9D6-A249"],
        },
        "Filestore": {
            "base_rate": 0.16,
            "operations": ["Basic", "Enterprise", "HighScale", "Zonal", "Regional"],
            "price_range": (0.13, 0.30),
            "pricing_model": "usage",
            "unit": "GiB-month",
            "usage_types": ["Basic", "Enterprise", "HighScale"],
            "sku_name_pattern": "Filestore {operation} in {region}",
            "sku_ids": ["D62B-F23A-A83D", "A8F3-C724-B861"],
        },
    },
    "Database": {
        "CloudSQL": {
            "base_rate": 0.0364,
            "operations": ["MySQL", "PostgreSQL", "SQLServer", "ComputeOptimized", "Storage", "HA"],
            "price_range": (0.03, 1.2),
            "pricing_model": "on_demand",
            "unit": "hour",
            "usage_types": ["DatabaseInstance", "Storage", "Backup", "Network"],
            "sku_name_pattern": "Cloud SQL {operation} in {region}",
            "sku_ids": ["7E87-A3AC-9734", "8A73-48CF-B313", "C384-82DA-5A42"],
        },
        "CloudSpanner": {
            "base_rate": 0.90,
            "operations": ["ProcessingUnits", "Storage", "Backup"],
            "price_range": (0.30, 1.5),
            "pricing_model": "on_demand",
            "unit": "node-hour",
            "usage_types": ["Nodes", "ProcessingUnits", "Storage", "Backup"],
            "sku_name_pattern": "Cloud Spanner {operation} in {region}",
            "sku_ids": ["D1F2-B728-5A71", "9A47-8FD3-C1A8"],
        },
        "Firestore": {
            "base_rate": 0.18,
            "operations": ["Storage", "Reads", "Writes", "Deletes", "Network"],
            "price_range": (0.10, 0.30),
            "pricing_model": "usage",
            "unit": "GiB-month",
            "usage_types": ["Storage", "Reads", "Writes", "Deletes", "Network"],
            "sku_name_pattern": "Firestore {operation} in {region}",
            "sku_ids": ["F58A-E8D3-A94B", "B3D2-C47A-92F5"],
        },
        "Bigtable": {
            "base_rate": 0.65,
            "operations": ["NodeHour", "SSD", "HDD", "Backup", "Restore"],
            "price_range": (0.30, 0.90),
            "pricing_model": "on_demand",
            "unit": "node-hour",
            "usage_types": ["NodeHours", "StorageSSD", "StorageHDD"],
            "sku_name_pattern": "Bigtable {operation} in {region}",
            "sku_ids": ["C2A8-F3D7-5E82", "D7F3-A159-C246"],
        },
        "Memorystore": {
            "base_rate": 0.049,
            "operations": ["Redis", "Memcached", "Standard", "HighAvailability"],
            "price_range": (0.025, 0.35),
            "pricing_model": "on_demand",
            "unit": "GB-hour",
            "usage_types": ["InstanceHours", "Network"],
            "sku_name_pattern": "Memorystore {operation} in {region}",
            "sku_ids": ["9B3A-F7DC-E8A2", "A8D2-F74C-B9E3"],
        },
    },
    "Analytics": {
        "BigQuery": {
            "base_rate": 0.02,
            "operations": ["Storage", "Analysis", "Streaming", "BI_Engine", "ML"],
            "price_range": (0.01, 0.05),
            "pricing_model": "usage",
            "unit": "TiB",
            "usage_types": ["ActiveStorage", "LongTermStorage", "Analysis", "Streaming"],
            "sku_name_pattern": "BigQuery {operation} in {region}",
            "sku_ids": ["5639-B2D4-6174", "95FF-2EF5-5EA1", "C1D7-8D28-4658"],
        },
        "Dataflow": {
            "base_rate": 0.06,
            "operations": ["Batch", "Streaming", "Compute", "Memory", "PD", "Shuffle"],
            "price_range": (0.03, 0.09),
            "pricing_model": "usage",
            "unit": "vCPU-hour",
            "usage_types": ["Batch", "Streaming", "FlexRS"],
            "sku_name_pattern": "Dataflow {operation} in {region}",
            "sku_ids": ["8F89-D4E2-5CBA", "7A85-3C9F-D1B2"],
        },
        "Dataproc": {
            "base_rate": 0.01,
            "operations": ["Standard", "HighCPU", "HighMem", "Compute", "Preemptible"],
            "price_range": (0.005, 0.03),
            "pricing_model": "on_demand",
            "unit": "vCPU-hour",
            "usage_types": ["StandardInstance", "HighMemoryInstance", "HighCPUInstance"],
            "sku_name_pattern": "Dataproc {operation} in {region}",
            "sku_ids": ["D3F5-B7A9-4E82", "9C85-F3D2-E7B4"],
        },
        "Pub/Sub": {
            "base_rate": 0.04,
            "operations": ["Message", "Storage", "Snapshot", "Seek"],
            "price_range": (0.02, 0.06),
            "pricing_model": "usage",
            "unit": "TiB",
            "usage_types": ["MessageDelivery", "Storage", "Snapshot"],
            "sku_name_pattern": "Pub/Sub {operation} in {region}",
            "sku_ids": ["E5A9-2D3B-7C8F", "B7D3-A2F8-C951"],
        },
        "Datastream": {
            "base_rate": 0.08,
            "operations": ["StreamingBytes", "NetBytes", "Storage"],
            "price_range": (0.04, 0.12),
            "pricing_model": "usage",
            "unit": "GiB",
            "usage_types": ["StreamingData", "NetworkData"],
            "sku_name_pattern": "Datastream {operation} in {region}",
            "sku_ids": ["F5E2-D7C8-9A3B", "C5D9-8F3A-E7B2"],
        },
    },
    "Networking": {
        "CloudVPN": {
            "base_rate": 0.05,
            "operations": ["Tunnel", "Traffic", "Endpoint", "HA"],
            "price_range": (0.03, 0.075),
            "pricing_model": "hourly",
            "unit": "hour",
            "usage_types": ["TunnelHours", "DataTransfer"],
            "sku_name_pattern": "Cloud VPN {operation} in {region}",
            "sku_ids": ["D7C9-A3B5-E2F4", "8F3E-D2C7-A5B9"],
        },
        "CloudInterconnect": {
            "base_rate": 0.042,
            "operations": ["Interconnect", "VLAN", "Traffic", "Redundancy"],
            "price_range": (0.03, 0.06),
            "pricing_model": "hourly",
            "unit": "hour",
            "usage_types": ["ConnectionHours", "DataTransfer"],
            "sku_name_pattern": "Cloud Interconnect {operation} in {region}",
            "sku_ids": ["E2D5-C9F3-A7B8", "A9F3-E7D2-C8B5"],
        },
        "CloudNAT": {
            "base_rate": 0.044,
            "operations": ["Gateway", "Traffic", "Endpoint"],
            "price_range": (0.03, 0.06),
            "pricing_model": "hourly",
            "unit": "hour",
            "usage_types": ["GatewayHour", "DataProcessed"],
            "sku_name_pattern": "Cloud NAT {operation} in {region}",
            "sku_ids": ["C9D5-A3F8-E2B7", "F2B8-D3C9-A7E5"],
        },
        "CloudLoadBalancing": {
            "base_rate": 0.025,
            "operations": ["ForwardingRule", "IngressData", "EgressData"],
            "price_range": (0.01, 0.04),
            "pricing_model": "hourly",
            "unit": "hour",
            "usage_types": ["ForwardingRuleHours", "DataProcessing"],
            "sku_name_pattern": "Cloud Load Balancing {operation} in {region}",
            "sku_ids": ["A2D8-F3C9-E5B7", "D5E7-C9B3-F2A8"],
        },
        "CloudCDN": {
            "base_rate": 0.075,
            "operations": ["CacheEgress", "LookupRequests", "CacheFill", "Invalidation"],
            "price_range": (0.04, 0.10),
            "pricing_model": "usage",
            "unit": "GiB",
            "usage_types": ["CacheEgress", "CacheLookups", "CacheFill"],
            "sku_name_pattern": "Cloud CDN {operation} in {region}",
            "sku_ids": ["F3B8-C2D5-A9E7", "E7A9-D2C5-B3F8"],
        },
        "VPC": {
            "base_rate": 0.01,
            "operations": ["EndpointOperations", "NATOperations", "DataTransfer", "VPNOperations"],
            "price_range": (0.005, 0.1),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["VPCEndpointHours", "NATGatewayHours", "DataProcessed-GB", "VPNConnectionHours"],
            "sku_name_pattern": "VPC {operation} in {region}",
            "sku_ids": ["E5B7-A2D8-F3C9", "F2A8-D5E7-C9B3"],
        },
        "CloudDNS": {
            "base_rate": 0.5,
            "operations": ["DNSOperations", "ZoneManagement", "HealthCheckOperations"],
            "price_range": (0.1, 2.0),
            "pricing_model": "on_demand",
            "unit": "Months",
            "usage_types": ["HostedZoneMonths", "Queries", "HealthChecks"],
            "sku_name_pattern": "Cloud DNS {operation} in {region}",
            "sku_ids": ["C9B3-F2A8-D5E7", "A2D8-F3C9-E5B7"],
        },
        "CloudArmor": {
            "base_rate": 5.0,
            "operations": ["WebRequestProcessing", "RuleManagement", "RuleSetManagement"],
            "price_range": (1.0, 10.0),
            "pricing_model": "on_demand",
            "unit": "Months",
            "usage_types": ["RuleMonths", "Requests", "RuleSetMonths"],
            "sku_name_pattern": "Cloud Armor {operation} in {region}",
            "sku_ids": ["F3C9-E5B7-A2D8", "D5E7-C9B3-F2A8"],
        },
    },
    "MachineLearning": {
        "VertexAI": {
            "base_rate": 0.28,
            "operations": ["Training", "Prediction", "AutoML", "Notebooks", "Metadata"],
            "price_range": (0.15, 0.50),
            "pricing_model": "on_demand",
            "unit": "hour",
            "usage_types": ["TrainingNodeHours", "PredictionNodeHours", "AutoML"],
            "sku_name_pattern": "Vertex AI {operation} in {region}",
            "sku_ids": ["D5F8-E2C7-A9B3", "B7E3-C9F5-D2A8"],
        },
        "AIProtagonist": {
            "base_rate": 0.0008,
            "operations": ["TextEmbeddings", "TextGeneration", "TextClassification", "Translation"],
            "price_range": (0.0003, 0.0015),
            "pricing_model": "usage",
            "unit": "1000 characters",
            "usage_types": ["Embeddings", "Generation", "Classification"],
            "sku_name_pattern": "AI Protagonist {operation} in {region}",
            "sku_ids": ["F8D3-E2C7-B5A9", "C7B5-D3F8-A2E9"],
        },
        "SpeechToText": {
            "base_rate": 0.006,
            "operations": ["Recognition", "AdaptedModels", "EnhancedModels", "Medical"],
            "price_range": (0.004, 0.009),
            "pricing_model": "usage",
            "unit": "15 seconds",
            "usage_types": ["StandardRecognition", "EnhancedRecognition", "MedicalRecognition"],
            "sku_name_pattern": "Speech-to-Text {operation} in {region}",
            "sku_ids": ["E9F5-C7D3-B2A8", "B2F8-D7C3-A9E5"],
        },
        "DialogFlow": {
            "base_rate": 0.002,
            "operations": ["TextQueries", "VoiceQueries", "AdvancedFeatures"],
            "price_range": (0.001, 0.004),
            "pricing_model": "usage",
            "unit": "request",
            "usage_types": ["TextRequests", "VoiceRequests", "AgentTraining"],
            "sku_name_pattern": "Dialogflow {operation} in {region}",
            "sku_ids": ["D2F7-E9C3-B5A8", "F5B2-C7D3-A8E9"],
        },
    },
    "Management": {
        "CloudMonitoring": {
            "base_rate": 0.258,
            "operations": ["IngestedData", "MetricsReads", "Dashboard", "AlertPolicy"],
            "price_range": (0.20, 0.30),
            "pricing_model": "usage",
            "unit": "MiB",
            "usage_types": ["IngestedVolume", "MetricsReads", "APIRequests"],
            "sku_name_pattern": "Cloud Monitoring {operation} in {region}",
            "sku_ids": ["B5E9-F2D7-C3A8", "D3F8-A7E2-B9C5"],
        },
        "CloudLogging": {
            "base_rate": 0.50,
            "operations": ["Storage", "Streaming", "Analysis", "Exporting"],
            "price_range": (0.30, 0.70),
            "pricing_model": "usage",
            "unit": "GiB",
            "usage_types": ["LogStorage", "LogStreaming", "LogAnalysis"],
            "sku_name_pattern": "Cloud Logging {operation} in {region}",
            "sku_ids": ["E5B9-D2F7-C3A8", "F7D3-B2E5-A9C8"],
        },
        "CloudTracing": {
            "base_rate": 0.20,
            "operations": ["Trace", "Span", "Insight"],
            "price_range": (0.15, 0.30),
            "pricing_model": "usage",
            "unit": "million spans",
            "usage_types": ["Traces", "Spans", "Insights"],
            "sku_name_pattern": "Cloud Trace {operation} in {region}",
            "sku_ids": ["B2F5-E9D3-C7A8", "D7E3-F5B9-A2C8"],
        },
        "ErrorReporting": {
            "base_rate": 0.01,
            "operations": ["Events", "Aggregation", "Analysis"],
            "price_range": (0.005, 0.02),
            "pricing_model": "usage",
            "unit": "events",
            "usage_types": ["ErrorEvents", "ErrorAnalysis"],
            "sku_name_pattern": "Error Reporting {operation} in {region}",
            "sku_ids": ["F3B8-E5D2-C7A9", "D2C7-F5B8-E3A9"],
        },
        "CloudTrace": {
            "base_rate": 0.20,
            "operations": ["Trace", "Span", "Insight"],
            "price_range": (0.15, 0.30),
            "pricing_model": "usage",
            "unit": "million spans",
            "usage_types": ["Traces", "Spans", "Insights"],
            "sku_name_pattern": "Cloud Trace {operation} in {region}",
            "sku_ids": ["E9D3-C7A8-B2F5", "F5B9-A2C8-D7E3"],
        },
        "CloudBilling": {
            "base_rate": 0.01,
            "operations": ["APIRequests", "ReportGeneration", "BudgetAlerts"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "APIRequest",
            "usage_types": ["BillingAPI-Request", "BillingReport"],
            "sku_name_pattern": "Cloud Billing {operation}",
            "sku_ids": ["C7A8-B2F5-E9D3", "A2C8-D7E3-F5B9"],
        },
        "ManagedGrafana": {
            "base_rate": 9.0,
            "operations": ["DashboardingOperations"],
            "price_range": (5.0, 15.0),
            "pricing_model": "monthly",
            "unit": "Users-Month",
            "usage_types": ["ManagedGrafana-ActiveUsers"],
            "sku_name_pattern": "Managed Grafana {operation} in {region}",
            "sku_ids": ["B2F5-E9D3-C7A8", "D7E3-F5B9-A2C8"],
        },
    },
    "Security": {
        "SecurityCommandCenter": {
            "base_rate": 0.10,
            "operations": ["Standard", "Premium", "Enterprise", "Analysis"],
            "price_range": (0.05, 0.20),
            "pricing_model": "monthly",
            "unit": "asset",
            "usage_types": ["StandardAssets", "PremiumAssets", "EnterpriseAssets"],
            "sku_name_pattern": "Security Command Center {operation} in {region}",
            "sku_ids": ["D7F3-B5E9-C2A8", "E9B5-F2D7-A3C8"],
        },
        "SecretManager": {
            "base_rate": 0.06,
            "operations": ["SecretVersion", "AccessRequest", "Rotation"],
            "price_range": (0.03, 0.10),
            "pricing_model": "monthly",
            "unit": "version",
            "usage_types": ["SecretVersions", "AccessOperations"],
            "sku_name_pattern": "Secret Manager {operation} in {region}",
            "sku_ids": ["E2D7-F5B9-C3A8", "B9F3-D7E2-A5C8"],
        },
        "IAM": {
            "base_rate": 0.05,
            "operations": ["Policy", "Binding", "Condition", "WorkloadIdentity"],
            "price_range": (0.03, 0.08),
            "pricing_model": "monthly",
            "unit": "binding",
            "usage_types": ["PolicyBinding", "WorkloadIdentity"],
            "sku_name_pattern": "IAM {operation} in {region}",
            "sku_ids": ["F5B9-D2E7-C3A8", "B2F5-E7D3-A9C8"],
        },
        "KeyManagementService": {
            "base_rate": 0.06,
            "operations": ["KeyVersion", "Operation", "CMEK", "HSM"],
            "price_range": (0.03, 0.10),
            "pricing_model": "monthly",
            "unit": "key",
            "usage_types": ["KeyVersions", "CryptoOperations", "HSMProtection"],
            "sku_name_pattern": "Key Management Service {operation} in {region}",
            "sku_ids": ["D7E3-F5B9-C2A8", "B5F2-D7E3-C9A8"],
        },
        "CloudHSM": {
            "base_rate": 1.45,
            "operations": ["HSMInstance", "KeyOperations", "BackupOperations"],
            "price_range": (1.20, 2.0),
            "pricing_model": "hourly",
            "unit": "Hours",
            "usage_types": ["CloudHSM-InstanceHours", "CloudHSM-BackupStorage-GB"],
            "sku_name_pattern": "Cloud HSM {operation} in {region}",
            "sku_ids": ["C3A8-B9F3-D7E2", "A5C8-E2D7-F5B9"],
        },
        "Certificate Manager": {
            "base_rate": 0.75,
            "operations": ["CertificateIssuance", "CertificateRenewal"],
            "price_range": (0.0, 0.75),
            "pricing_model": "monthly",
            "unit": "Certificates-Month",
            "usage_types": ["CertificateManager-PrivateCertificateAuthority-Month"],
            "sku_name_pattern": "Certificate Manager {operation} in {region}",
            "sku_ids": ["F5B9-C3A8-B9F3", "D7E2-A5C8-E2D7"],
        },
    },
    "Data": {
        "ElasticSearch": {
            "base_rate": 0.10,
            "operations": ["ClusterHours", "StorageGB", "NetworkGB"],
            "price_range": (0.05, 2.0),
            "pricing_model": "on_demand",
            "unit": "Hours",
            "usage_types": ["ElasticSearch-ClusterHours", "ElasticSearch-Storage-GB"],
            "sku_name_pattern": "Elastic Search {operation} in {region}",
            "sku_ids": ["B9F3-D7E2-A5C8", "E2D7-F5B9-C3A8"],
        },
        "Looker": {
            "base_rate": 12.0,
            "operations": ["DashboardUsage", "DataUsage"],
            "price_range": (5.0, 25.0),
            "pricing_model": "monthly",
            "unit": "Months",
            "usage_types": ["Looker-UserMonths", "Looker-Data-GB"],
            "sku_name_pattern": "Looker {operation} in {region}",
            "sku_ids": ["D7E2-A5C8-B9F3", "F5B9-C3A8-E2D7"],
        },
    },
    "Healthcare": {
        "HealthLake": {
            "base_rate": 0.01,
            "operations": ["DataStorage", "DataImport", "DataQuery"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": ["HealthLake-Storage-GB-Month", "HealthLake-DataProcessing-GB"],
            "sku_name_pattern": "Health Lake {operation} in {region}",
            "sku_ids": ["A5C8-B9F3-D7E2", "C3A8-E2D7-F5B9"],
        },
    },
    "Media": {
        "MediaConvert": {
            "base_rate": 0.0075,
            "operations": ["VideoConversion", "AudioConversion", "Packaging"],
            "price_range": (0.005, 0.015),
            "pricing_model": "on_demand",
            "unit": "Minutes",
            "usage_types": ["MediaConvert-SD", "MediaConvert-HD", "MediaConvert-UHD"],
            "sku_name_pattern": "Media Convert {operation} in {region}",
            "sku_ids": ["B9F3-D7E2-A5C8", "E2D7-F5B9-C3A8"],
        },
        "MediaPackage": {
            "base_rate": 0.04,
            "operations": ["Ingest", "Origination", "Storage"],
            "price_range": (0.02, 0.08),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["MediaPackage-Ingest-GB", "MediaPackage-Egress-GB"],
            "sku_name_pattern": "Media Package {operation} in {region}",
            "sku_ids": ["D7E2-A5C8-B9F3", "F5B9-C3A8-E2D7"],
        },
        "MediaLive": {
            "base_rate": 0.2813,
            "operations": ["ChannelHours", "InputProcessing", "OutputProcessing"],
            "price_range": (0.15, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hours",
            "usage_types": ["MediaLive-ChannelHours-SD", "MediaLive-ChannelHours-HD", "MediaLive-ChannelHours-UHD"],
            "sku_name_pattern": "Media Live {operation} in {region}",
            "sku_ids": ["A5C8-B9F3-D7E2", "C3A8-E2D7-F5B9"],
        },
        "MediaConnect": {
            "base_rate": 0.08,
            "operations": ["FlowHours", "OutputHours", "DataTransfer"],
            "price_range": (0.05, 0.15),
            "pricing_model": "on_demand",
            "unit": "Hours",
            "usage_types": ["MediaConnect-FlowHours", "MediaConnect-OutputHours", "MediaConnect-DataTransfer-GB"],
            "sku_name_pattern": "Media Connect {operation} in {region}",
            "sku_ids": ["B9F3-D7E2-A5C8", "E2D7-F5B9-C3A8"],
        },
        "Elemental": {
            "base_rate": 0.15,
            "operations": ["EncodingHours", "TranscodingHours", "OutputHours"],
            "price_range": (0.10, 0.30),
            "pricing_model": "on_demand",
            "unit": "Hours",
            "usage_types": ["Elemental-EncodingHours", "Elemental-OutputHours"],
            "sku_name_pattern": "Elemental {operation} in {region}",
            "sku_ids": ["D7E2-A5C8-B9F3", "F5B9-C3A8-E2D7"],
        },
    },
    "Location": {
        "Location": {
            "base_rate": 0.04,
            "operations": ["Maps", "Places", "Routes", "Tracking", "Geofencing"],
            "price_range": (0.02, 0.08),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": ["Location-MapTiles", "Location-Geocoding", "Location-Routes", "Location-Tracking"],
            "sku_name_pattern": "Location {operation} in {region}",
            "sku_ids": ["A5C8-B9F3-D7E2", "C3A8-E2D7-F5B9"],
        },
    },
    "ApplicationServices": {
        "Anthos": {
            "base_rate": 0.10,
            "operations": ["Cluster", "Management", "Runtime", "Service"],
            "price_range": (0.05, 0.20),
            "pricing_model": "monthly",
            "unit": "vCPU",
            "usage_types": ["ClusterOperations", "ManagementOperations"],
            "sku_name_pattern": "Anthos {operation} in {region}",
            "sku_ids": ["E7D3-F5B9-C2A8", "B9F3-D7E2-C5A8"],
        },
        "CloudTasks": {
            "base_rate": 0.40,
            "operations": ["Operations", "Storage", "Scheduling"],
            "price_range": (0.30, 0.50),
            "pricing_model": "usage",
            "unit": "million operations",
            "usage_types": ["TaskOperations", "TaskStorage"],
            "sku_name_pattern": "Cloud Tasks {operation} in {region}",
            "sku_ids": ["F5B9-D2E7-C3A8", "B2F5-E7D3-A9C8"],
        },
        "CloudScheduler": {
            "base_rate": 0.10,
            "operations": ["Jobs", "Executions", "Attempts"],
            "price_range": (0.05, 0.20),
            "pricing_model": "monthly",
            "unit": "job",
            "usage_types": ["JobOperations", "JobExecutions"],
            "sku_name_pattern": "Cloud Scheduler {operation} in {region}",
            "sku_ids": ["D7E3-F5B9-C2A8", "B5F2-D7E3-C9A8"],
        },
        "AppMesh": {
            "base_rate": 0.012,
            "operations": ["MeshEndpoints", "VirtualNodes", "VirtualServices"],
            "price_range": (0.01, 0.02),
            "pricing_model": "hourly",
            "unit": "Resources-Hours",
            "usage_types": ["AppMesh-ResourceHours", "AppMesh-DataProcessed-GB"],
            "sku_name_pattern": "App Mesh {operation} in {region}",
            "sku_ids": ["C4D6-F3B7-A2E9", "E9A2-D4F3-C7B8"],
        },
        "ApiGateway": {
            "base_rate": 3.5,
            "operations": ["APIOperations", "DataTransfer"],
            "price_range": (1.0, 5.0),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": ["APICalls", "APIGatewayDataTransfer-Out"],
            "sku_name_pattern": "API Gateway {operation} in {region}",
            "sku_ids": ["F9B3-D7E2-A5C8", "E5A2-F9B3-D7C8"],
        },
        "BatchService": {
            # Free service (pay only for underlying resources)
            "base_rate": 0.0,
            "operations": ["SubmitJob", "ManageJob", "ScheduleJob"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Jobs",
            "usage_types": ["Batch-JobSubmissions", "Batch-JobScheduling"],
            "sku_name_pattern": "Batch Service {operation} in {region}",
            "sku_ids": ["E7A2-B9F4-C3D8", "D8C3-F4B9-A2E7"],
        },
    },
    "DevOps": {
        "CloudBuild": {
            "base_rate": 0.005,
            "operations": ["BuildExecution", "BatchBuild"],
            "price_range": (0.001, 0.01),
            "pricing_model": "on_demand",
            "unit": "BuildMinute",
            "usage_types": ["BuildMinutes", "ComputeType"],
            "sku_name_pattern": "Cloud Build {operation} in {region}",
            "sku_ids": ["F4B9-A2E7-D3C8", "C8D3-E7A2-F4B9"],
        },
        "DeploymentManager": {
            "base_rate": 0.0,  # Free service
            "operations": ["DeploymentOperations", "TemplateOperations"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Operations",
            "usage_types": ["DeploymentOperations"],
            "sku_name_pattern": "Deployment Manager {operation} in {region}",
            "sku_ids": ["A2E7-F4B9-D3C8", "D3C8-A2E7-F4B9"],
        },
    },
    "IoT": {
        "IoT": {
            "base_rate": 0.08,
            "operations": ["MessageBroker", "DeviceRegistry", "RulesEngine"],
            "price_range": (0.05, 0.15),
            "pricing_model": "on_demand",
            "unit": "Million Messages",
            "usage_types": ["IoT-Messages", "IoT-Rules", "IoT-DeviceRegistry"],
            "sku_name_pattern": "IoT Core {operation} in {region}",
            "sku_ids": ["B9F4-C3D8-E7A2", "A2E7-D3C8-F4B9"],
        },
        "IoTSiteWise": {
            "base_rate": 0.10,
            "operations": ["DataCollection", "DataProcessing", "DataStorage"],
            "price_range": (0.05, 0.20),
            "pricing_model": "on_demand",
            "unit": "DataPoints",
            "usage_types": ["IoTSiteWise-DataPoints", "IoTSiteWise-Storage-GB-Month"],
            "sku_name_pattern": "IoT SiteWise {operation} in {region}",
            "sku_ids": ["C3D8-E7A2-B9F4", "F4B9-C3D8-E7A2"],
        },
        "IoTAnalytics": {
            "base_rate": 0.25,
            "operations": ["DataIngestion", "DataStorage", "DataProcessing"],
            "price_range": (0.10, 0.50),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["IoTAnalytics-Messages", "IoTAnalytics-Storage-GB-Month"],
            "sku_name_pattern": "IoT Analytics {operation} in {region}",
            "sku_ids": ["E7A2-B9F4-C3D8", "D8C3-F4B9-A2E7"],
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

# GCP's organizational structure is different from AWS:
# Organization > Folders > Projects (with billing accounts)
ORGANIZATION_STRUCTURE = {
    "Organization": {
        "name": "example-organization",
        "org_id": "12345678901",
        "folders": {
            "Core": {
                "folder_id": "98765432101",
                "projects": {
                    "Security": {
                        "project_id": "security-central-555555",
                        "project_number": "555555555555"
                    },
                    "SharedServices": {
                        "project_id": "shared-services-666666",
                        "project_number": "666666666666"
                    },
                    "Compliance": {
                        "project_id": "compliance-777777",
                        "project_number": "777777777777"
                    }
                }
            },
            "BusinessUnits": {
                "folder_id": "87654321098",
                "subfolders": {
                    "Aviation": {
                        "folder_id": "76543210987",
                        "projects": {
                            "Aviation-Dev": {
                                "project_id": "aviation-dev-222201",
                                "project_number": "222200000001"
                            },
                            "Aviation-Staging": {
                                "project_id": "aviation-staging-333301",
                                "project_number": "333300000001"
                            },
                            "Aviation-Prod": {
                                "project_id": "aviation-prod-444401",
                                "project_number": "444400000001"
                            },
                            "Aviation-Analytics": {
                                "project_id": "aviation-analytics-888801",
                                "project_number": "888800000001"
                            },
                            "Aviation-IoT": {
                                "project_id": "aviation-iot-999901",
                                "project_number": "999900000001"
                            }
                        }
                    },
                    "Pharma": {
                        "folder_id": "65432109876",
                        "projects": {
                            "Pharma-Dev": {
                                "project_id": "pharma-dev-222202",
                                "project_number": "222200000002"
                            },
                            "Pharma-Staging": {
                                "project_id": "pharma-staging-333302",
                                "project_number": "333300000002"
                            },
                            "Pharma-Prod": {
                                "project_id": "pharma-prod-444402",
                                "project_number": "444400000002"
                            },
                            "Pharma-Research": {
                                "project_id": "pharma-research-888802",
                                "project_number": "888800000002"
                            },
                            "Pharma-Logistics": {
                                "project_id": "pharma-logistics-999902",
                                "project_number": "999900000002"
                            }
                        }
                    },
                    "Manufacturing": {
                        "folder_id": "54321098765",
                        "projects": {
                            "Manufacturing-Dev": {
                                "project_id": "manufacturing-dev-222203",
                                "project_number": "222200000003"
                            },
                            "Manufacturing-Staging": {
                                "project_id": "manufacturing-stg-333303",
                                "project_number": "333300000003"
                            },
                            "Manufacturing-Prod": {
                                "project_id": "manufacturing-prod-444403",
                                "project_number": "444400000003"
                            },
                            "Manufacturing-IoT": {
                                "project_id": "manufacturing-iot-888803",
                                "project_number": "888800000003"
                            },
                            "Manufacturing-Logistics": {
                                "project_id": "manufacturing-logs-999903",
                                "project_number": "999900000003"
                            }
                        }
                    },
                    "SupplyChain": {
                        "folder_id": "43210987654",
                        "projects": {
                            "SupplyChain-Dev": {
                                "project_id": "supplychain-dev-222204",
                                "project_number": "222200000004"
                            },
                            "SupplyChain-Staging": {
                                "project_id": "supplychain-stg-333304",
                                "project_number": "333300000004"
                            },
                            "SupplyChain-Prod": {
                                "project_id": "supplychain-prod-444404",
                                "project_number": "444400000004"
                            },
                            "SupplyChain-Logistics": {
                                "project_id": "supplychain-logs-888804",
                                "project_number": "888800000004"
                            },
                            "SupplyChain-Analytics": {
                                "project_id": "supplychain-analytics-999904",
                                "project_number": "999900000004"
                            }
                        }
                    },
                    "SoftwareSolutions": {
                        "folder_id": "32109876543",
                        "projects": {
                            "SoftwareSolutions-Dev": {
                                "project_id": "swsolutions-dev-222205",
                                "project_number": "222200000005"
                            },
                            "SoftwareSolutions-Staging": {
                                "project_id": "swsolutions-stg-333305",
                                "project_number": "333300000005"
                            },
                            "SoftwareSolutions-Prod": {
                                "project_id": "swsolutions-prod-444405",
                                "project_number": "444400000005"
                            },
                            "SoftwareSolutions-CustomerData": {
                                "project_id": "swsolutions-data-888805",
                                "project_number": "888800000005"
                            },
                            "SoftwareSolutions-Analytics": {
                                "project_id": "swsolutions-analytics-999905",
                                "project_number": "999900000005"
                            }
                        }
                    },
                    "MachineLearning": {
                        "folder_id": "21098765432",
                        "projects": {
                            "ML-Dev": {
                                "project_id": "ml-dev-222206",
                                "project_number": "222200000006"
                            },
                            "ML-Staging": {
                                "project_id": "ml-staging-333306",
                                "project_number": "333300000006"
                            },
                            "ML-Prod": {
                                "project_id": "ml-prod-444406",
                                "project_number": "444400000006"
                            },
                            "ML-FeatureStore": {
                                "project_id": "ml-featurestore-888806",
                                "project_number": "888800000006"
                            },
                            "ML-Analytics": {
                                "project_id": "ml-analytics-999906",
                                "project_number": "999900000006"
                            }
                        }
                    }
                }
            },
            "Sandbox": {
                "folder_id": "10987654321",
                "projects": {
                    "Sandbox-Central": {
                        "project_id": "sandbox-central-222299",
                        "project_number": "222299999999"
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
PROJECT_BILLING_MAPPING = {
    # Development environments use the development billing account
    "aviation-dev-222201": "development",
    "pharma-dev-222202": "development",
    "manufacturing-dev-222203": "development",
    "supplychain-dev-222204": "development",
    "swsolutions-dev-222205": "development",
    "ml-dev-222206": "development",
    "sandbox-central-222299": "development",

    # Map by project display names too
    "Aviation-Dev": "development",
    "Pharma-Dev": "development",
    "Manufacturing-Dev": "development",
    "SupplyChain-Dev": "development",
    "SoftwareSolutions-Dev": "development",
    "ML-Dev": "development",
    "Sandbox-Central": "development",

    # Research projects use the research billing account
    "pharma-research-888802": "research",
    "ml-featurestore-888806": "research",
    "Pharma-Research": "research",
    "ML-FeatureStore": "research",

    # By stage patterns
    "dev": "development",
    "sandbox": "development",
    "research": "research",
    "featurestore": "research",

    # All other projects use the primary billing account (default)
}

# Create a direct mapping between stages and projects
STAGE_TO_PROJECT_MAPPING = {
    # Aviation
    "aviation-dev": {"project_id": "aviation-dev-222201", "project_number": "222200000001", "project_name": "Aviation Dev"},
    "aviation-staging": {"project_id": "aviation-staging-333301", "project_number": "333300000001", "project_name": "Aviation Staging"},
    "aviation-prod": {"project_id": "aviation-prod-444401", "project_number": "444400000001", "project_name": "Aviation Production"},
    "aviation-analytics": {"project_id": "aviation-analytics-888801", "project_number": "888800000001", "project_name": "Aviation Analytics"},
    "aviation-iot": {"project_id": "aviation-iot-999901", "project_number": "999900000001", "project_name": "Aviation IoT"},

    # Pharma
    "pharma-dev": {"project_id": "pharma-dev-222202", "project_number": "222200000002", "project_name": "Pharma Dev"},
    "pharma-staging": {"project_id": "pharma-staging-333302", "project_number": "333300000002", "project_name": "Pharma Staging"},
    "pharma-prod": {"project_id": "pharma-prod-444402", "project_number": "444400000002", "project_name": "Pharma Production"},
    "pharma-research": {"project_id": "pharma-research-888802", "project_number": "888800000002", "project_name": "Pharma Research"},
    "pharma-logistics": {"project_id": "pharma-logistics-999902", "project_number": "999900000002", "project_name": "Pharma Logistics"},

    # Manufacturing
    "manufacturing-dev": {"project_id": "manufacturing-dev-222203", "project_number": "222200000003", "project_name": "Manufacturing Dev"},
    "manufacturing-staging": {"project_id": "manufacturing-stg-333303", "project_number": "333300000003", "project_name": "Manufacturing Staging"},
    "manufacturing-prod": {"project_id": "manufacturing-prod-444403", "project_number": "444400000003", "project_name": "Manufacturing Production"},
    "manufacturing-iot": {"project_id": "manufacturing-iot-888803", "project_number": "888800000003", "project_name": "Manufacturing IoT"},
    "manufacturing-logistics": {"project_id": "manufacturing-logs-999903", "project_number": "999900000003", "project_name": "Manufacturing Logistics"},

    # SupplyChain
    "supplychain-dev": {"project_id": "supplychain-dev-222204", "project_number": "222200000004", "project_name": "Supply Chain Dev"},
    "supplychain-staging": {"project_id": "supplychain-stg-333304", "project_number": "333300000004", "project_name": "Supply Chain Staging"},
    "supplychain-prod": {"project_id": "supplychain-prod-444404", "project_number": "444400000004", "project_name": "Supply Chain Production"},
    "supplychain-logistics": {"project_id": "supplychain-logs-888804", "project_number": "888800000004", "project_name": "Supply Chain Logistics"},
    "supplychain-analytics": {"project_id": "supplychain-analytics-999904", "project_number": "999900000004", "project_name": "Supply Chain Analytics"},

    # SoftwareSolutions
    "softwaresolutions-dev": {"project_id": "swsolutions-dev-222205", "project_number": "222200000005", "project_name": "Software Solutions Dev"},
    "softwaresolutions-staging": {"project_id": "swsolutions-stg-333305", "project_number": "333300000005", "project_name": "Software Solutions Staging"},
    "softwaresolutions-prod": {"project_id": "swsolutions-prod-444405", "project_number": "444400000005", "project_name": "Software Solutions Production"},
    "softwaresolutions-customerdata": {"project_id": "swsolutions-data-888805", "project_number": "888800000005", "project_name": "Software Solutions Customer Data"},
    "softwaresolutions-analytics": {"project_id": "swsolutions-analytics-999905", "project_number": "999900000005", "project_name": "Software Solutions Analytics"},

    # MachineLearning
    "ml-dev": {"project_id": "ml-dev-222206", "project_number": "222200000006", "project_name": "Machine Learning Dev"},
    "ml-staging": {"project_id": "ml-staging-333306", "project_number": "333300000006", "project_name": "Machine Learning Staging"},
    "ml-prod": {"project_id": "ml-prod-444406", "project_number": "444400000006", "project_name": "Machine Learning Production"},
    "ml-featurestore": {"project_id": "ml-featurestore-888806", "project_number": "888800000006", "project_name": "Machine Learning Feature Store"},
    "ml-analytics": {"project_id": "ml-analytics-999906", "project_number": "999900000006", "project_name": "Machine Learning Analytics"},

    # Core Services
    "security": {"project_id": "security-central-555555", "project_number": "555555555555", "project_name": "Security Central"},
    "shared-services": {"project_id": "shared-services-666666", "project_number": "666666666666", "project_name": "Shared Services"},
    "compliance": {"project_id": "compliance-777777", "project_number": "777777777777", "project_name": "Compliance"},
    "sandbox-central": {"project_id": "sandbox-central-222299", "project_number": "222299999999", "project_name": "Sandbox Central"},
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
    "number_of_days": 365,
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

# Service Mapping from AWS to GCP (for project migration)
AWS_TO_GCP_SERVICE_MAPPING = {
    # Compute
    "EC2": "ComputeEngine",
    "Lambda": "CloudFunctions",
    "ECS": "CloudRun",
    "EKS": "GKE",
    "AutoScaling": "ComputeEngine",  # Managed with instance groups
    "ElasticBeanstalk": "AppEngine",

    # Storage
    "S3": "CloudStorage",
    "EBS": "PersistentDisk",
    "EFS": "Filestore",
    "Glacier": "CloudStorage",  # Archive storage class
    "Backup": "CloudStorage",  # With lifecycle policies

    # Database
    "RDS": "CloudSQL",
    "DynamoDB": "Firestore",
    "ElastiCache": "Memorystore",
    "Timestream": "BigQuery",

    # Analytics
    "Athena": "BigQuery",
    "DataBrew": "Dataflow",
    "EMR": "Dataproc",
    "Glue": "Dataflow",
    "KinesisDataAnalytics": "Dataflow",
    "KinesisDataStreams": "Pub/Sub",
    "KinesisDataFirehose": "Pub/Sub",
    "LakeFormation": "Dataflow",
    "MSK": "Pub/Sub",
    "QuickSight": "Looker",
    "Redshift": "BigQuery",

    # Integration
    "APIGateway": "ApiGateway",
    "AppSync": "ApiGateway",
    "Cognito": "IAM",
    "EventBridge": "Pub/Sub",
    "MQ": "Pub/Sub",
    "SNS": "Pub/Sub",
    "SQS": "Pub/Sub",
    "StepFunctions": "CloudScheduler",

    # Management & Governance
    "SystemsManager": "CloudMonitoring",
    "CloudWatch": "CloudMonitoring",
    "CloudWatchLogs": "CloudLogging",
    "CloudTrail": "CloudLogging",
    "CloudFormation": "DeploymentManager",
    "CostExplorer": "CloudBilling",

    # Networking
    "CloudFront": "CloudCDN",
    "DirectConnect": "CloudInterconnect",
    "NetworkFirewall": "CloudArmor",
    "Route53": "CloudDNS",
    "VPC": "VPC",

    # ML
    "Bedrock": "VertexAI",
    "Comprehend": "VertexAI",
    "Lex": "DialogFlow",
    "Rekognition": "VertexAI",
    "SageMaker": "VertexAI",
    "SageMakerFeatureStore": "VertexAI",
    "SageMakerGroundTruth": "VertexAI",
    "SageMakerInference": "VertexAI",

    # Security
    "AuditManager": "SecurityCommandCenter",
    "Config": "SecurityCommandCenter",
    "GuardDuty": "SecurityCommandCenter",
    "IAMAccessAnalyzer": "SecurityCommandCenter",
    "IAMIdentityCenter": "IAM",
    "Inspector": "SecurityCommandCenter",
    "KMS": "KeyManagementService",
    "SecurityHub": "SecurityCommandCenter",
    "SecurityLake": "SecurityCommandCenter",
    "ShieldAdvanced": "CloudArmor",
    "WAF": "CloudArmor",
    "SecretsManager": "SecretManager"
}

CONFIG = {
    "number_of_days": CONFIGURABLES["number_of_days"],
    "annual_budget": CONFIGURABLES["annual_budget"],
    "services": GCP_SERVICES,
    "use_case_scenarios": USE_CASE_SCENARIOS,
    "organization_structure": ORGANIZATION_STRUCTURE,
    "billing_accounts": BILLING_ACCOUNTS,
    "project_billing_mapping": PROJECT_BILLING_MAPPING,
    "STAGE_TO_PROJECT_MAPPING": STAGE_TO_PROJECT_MAPPING,
    "project_lifecycles": PROJECT_LIFECYCLES,
    "project_stages": PROJECT_STAGES,
    "configurables": CONFIGURABLES,
    "gcp_regions": GCP_REGIONS,
    "gcp_zones": GCP_ZONES,
    "regional_cost_factors": REGIONAL_COST_FACTORS,
    "aws_to_gcp_mapping": AWS_TO_GCP_SERVICE_MAPPING,
    "projects": {
        # Aviation Business Unit Projects
        "AerodynamicPerformanceAnalysis": {
            "description": "Aircraft aerodynamic performance analysis using cloud-based ETL and analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "Dataproc",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["aviation-analytics"],
            "business_unit": "Aviation",
        },
        "SkyConnectPassengerApp": {
            "description": "Mobile application for airline passengers providing flight information and services.",
            "use_case": "Mobile Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "CloudFunctions",
                "Firestore",
                "ApiGateway",
                "IAM",
                "CloudCDN",
                "Pub/Sub",
                "CloudLogging",
                "CloudArmor",
            ],
            "stages": ["aviation-prod", "aviation-dev"],
            "business_unit": "Aviation",
        },
        "GuardianAirTrafficControl": {
            "description": "Mission-critical air traffic control system ensuring safe and efficient flight operations.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "VPC",
                "CloudInterconnect",
                "CloudLogging",
                "CloudDNS",
            ],
            "stages": ["aviation-prod", "aviation-staging"],
            "business_unit": "Aviation",
        },
        "RunwayOperationsMonitoring": {
            "description": "Real-time monitoring and analytics of runway conditions and airport operations.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "growing",
            "services": [
                "CloudMonitoring",
                "ManagedGrafana",
                "CloudMonitoring",
                "CloudLogging",
                "CloudLogging",
            ],
            "stages": ["aviation-analytics"],
            "business_unit": "Aviation",
        },
        "JetEngineTelemetryAnalysis": {
            "description": "Advanced analytics of jet engine telemetry data for performance optimization and predictive maintenance.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "Pub/Sub",
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "BigQuery",
                "Dataproc",
                "CloudLogging",
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
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "ComputeEngine",
                "CloudStorage",
                "Dataflow",
                "Firestore",
                "VertexAI",
                "CloudLogging",
            ],
            "stages": ["pharma-research", "pharma-staging", "pharma-prod"],
            "business_unit": "Pharma",
        },
        "TrialMasterClinicalPlatform": {
            "description": "Comprehensive platform for managing and executing clinical trials, ensuring compliance and data integrity.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ApiGateway",
                "IAM",
                "CloudLogging",
                "CloudLogging",
                "CloudArmor",
                "Pub/Sub",
            ],
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "PillProductionQualityControl": {
            "description": "Machine learning system for real-time quality control in pharmaceutical pill production.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "Pub/Sub",
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "Dataproc",
                "BigQuery",
                "CloudLogging",
            ],
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "GenomeAnalyticsWorkbench": {
            "description": "Advanced workbench for genomic data analysis, enabling faster and more accurate research.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "Dataproc",
                "BigQuery",
                "Dataflow",
                "ComputeEngine",
                "CloudLogging",
            ],
            "stages": ["pharma-research", "pharma-analytics"],
            "business_unit": "Pharma",
        },
        "PersonalizedDrugRecommendationEngine": {
            "description": "Generative AI engine to provide personalized drug recommendations based on patient profiles.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "just_started",
            "services": [
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "DialogFlow",
                "CloudLogging",
            ],
            "stages": ["pharma-research"],
            "business_unit": "Pharma",
        },
        "GxPComplianceDashboard": {
            "description": "Dashboard to monitor and ensure GxP compliance across pharmaceutical production and research.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
            ],
            "stages": ["pharma-prod", "compliance"],
            "business_unit": "Pharma",
        },
        "MediSupplyChainTracker": {
            "description": "Real-time tracking and visibility platform for the medical supply chain, improving logistics and efficiency.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "Pub/Sub",
                "Pub/Sub",
                "Pub/Sub",
                "Firestore",
                "ApiGateway",
                "Looker",
                "CloudFunctions",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["pharma-logistics"],
            "business_unit": "Pharma",
        },
        "RDExperimentDataPipeline": {
            "description": "Automated data pipeline for managing and processing research and development experiment data.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "Dataflow",
                "CloudScheduler",
                "CloudStorage",
                "ComputeEngine",
                "VertexAI",
                "CloudLogging",
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
                "Pub/Sub",
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "Looker",
                "Dataproc",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["manufacturing-iot", "manufacturing-analytics", "manufacturing-prod"],
            "business_unit": "Manufacturing",
        },
        "EquipmentPredictiveMaintenance": {
            "description": "Predictive maintenance system using machine learning to forecast equipment failures and optimize maintenance schedules.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "CloudStorage",
                "Firestore",
                "Pub/Sub",
                "Looker",
                "CloudLogging",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging", "manufacturing-analytics"],
            "business_unit": "Manufacturing",
        },
        "ComponentSupplyChainVisibility": {
            "description": "Platform for enhanced visibility and tracking of components across the manufacturing supply chain.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "Pub/Sub",
                "Pub/Sub",
                "Pub/Sub",
                "Firestore",
                "ApiGateway",
                "Looker",
                "CloudFunctions",
                "CloudLogging",
            ],
            "stages": ["manufacturing-logistics", "manufacturing-prod"],
            "business_unit": "Manufacturing",
        },
        "AutomatedQualityInspection": {
            "description": "Automated visual quality inspection system for manufactured products using AI and computer vision.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "VertexAI",
                "CloudStorage",
                "CloudFunctions",
                "ApiGateway",
                "CloudScheduler",
                "CloudLogging",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging"],
            "business_unit": "Manufacturing",
        },
        "ProductionLineDashboard": {
            "description": "Real-time dashboard providing key performance indicators and operational insights for manufacturing production lines.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudMonitoring",
                "CloudLogging",
                "CloudMonitoring",
                "CloudTrace",
                "Pub/Sub",
            ],
            "stages": ["manufacturing-prod", "manufacturing-iot"],
            "business_unit": "Manufacturing",
        },
        "EnterpriseResourcePlanning": {
            "description": "Comprehensive ERP system to manage all aspects of manufacturing operations, from resource planning to financial management.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ComputeEngine",
                "VPC",
                "CloudInterconnect",
                "CloudLogging",
                "CloudLogging",
                "CloudDNS",
            ],
            "stages": ["manufacturing-prod", "manufacturing-staging"],
            "business_unit": "Manufacturing",
        },
        "FactoryFloorComplianceSystem": {
            "description": "System to ensure factory floor operations adhere to industry regulations and compliance standards.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
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
                "Pub/Sub",
                "Pub/Sub",
                "Pub/Sub",
                "Firestore",
                "ApiGateway",
                "Looker",
                "CloudFunctions",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["supplychain-logistics", "supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "WarehouseManagementApp": {
            "description": "Application for managing warehouse operations, inventory, and order fulfillment.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ComputeEngine",
                "VPC",
                "CloudCDN",
                "CloudArmor",
                "CloudLogging",
                "CloudDNS",
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "SupplierSelfServicePortal": {
            "description": "Self-service portal for suppliers to manage orders, invoices, and communication with the organization.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ApiGateway",
                "IAM",
                "CloudCDN",
                "CloudArmor",
                "CloudLogging",
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "DemandForecastAI": {
            "description": "AI-powered demand forecasting system to predict future demand and optimize inventory levels.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "VertexAI",
                "VertexAI",
                "VertexAI",
                "CloudStorage",
                "Dataflow",
                "BigQuery",
                "Looker",
                "CloudLogging",
            ],
            "stages": ["supplychain-analytics", "supplychain-staging", "supplychain-prod"],
            "business_unit": "SupplyChain",
        },
        "RouteOptimizationEngine": {
            "description": "Engine for optimizing delivery routes and logistics operations to reduce costs and improve delivery times.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "Dataflow",
                "BigQuery",
                "Dataproc",
                "BigQuery",
                "CloudStorage",
                "CloudScheduler",
                "CloudLogging",
            ],
            "stages": ["supplychain-logistics", "supplychain-analytics"],
            "business_unit": "SupplyChain",
        },
        "InventoryVisibilityPlatform": {
            "description": "Platform providing real-time visibility into inventory levels and locations across the entire supply chain network.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "Pub/Sub",
                "Pub/Sub",
                "BigQuery",
                "CloudStorage",
                "Looker",
                "CloudFunctions",
                "CloudLogging",
            ],
            "stages": ["supplychain-logistics", "supplychain-prod"],
            "business_unit": "SupplyChain",
        },
        "TradeComplianceMonitor": {
            "description": "System to monitor and ensure compliance with international trade regulations and tariffs.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
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
                "ComputeEngine",
                "CloudRun",
                "CloudSQL",
                "Firestore",
                "ComputeEngine",
                "ApiGateway",
                "CloudFunctions",
                "Memorystore",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "CustomerServiceHelpCenter": {
            "description": "Online help center and support portal for SaaS customers, offering knowledge base and ticketing system.",
            "use_case": "Software Solutions",
            "lifecycle": "peak_and_plateau",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ApiGateway",
                "IAM",
                "CloudCDN",
                "CloudArmor",
                "CloudLogging",
                "CloudDNS",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "TeamCollaborationHub": {
            "description": "Enterprise-grade team collaboration and communication platform for internal company use.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "ComputeEngine",
                "VPC",
                "CloudInterconnect",
                "CloudLogging",
                "CloudLogging",
                "CloudDNS",
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "SaaSCustomerInsights": {
            "description": "Analytics and business intelligence platform providing insights into SaaS customer usage and behavior.",
            "use_case": "Analytics",
            "lifecycle": "growing",
            "services": [
                "BigQuery",
                "Looker",
                "Dataflow",
                "CloudStorage",
                "BigQuery",
                "Dataproc",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-customerdata", "softwaresolutions-analytics", "softwaresolutions-prod"],
            "business_unit": "SoftwareSolutions",
        },
        "FeatureRolloutManager": {
            "description": "System to manage and control the rollout of new features to SaaS customers, enabling gradual releases and A/B testing.",
            "use_case": "Software Solutions",
            "lifecycle": "just_started",
            "services": [
                "CloudFunctions",
                "Firestore",
                "ApiGateway",
                "CloudScheduler",
                "Pub/Sub",
                "Pub/Sub",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-dev"],
            "business_unit": "SoftwareSolutions",
        },
        "CustomerDataLakehouse": {
            "description": "Scalable data lakehouse for storing and analyzing customer data to improve SaaS offering and customer experience.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "CloudStorage",
                "Dataflow",
                "Dataflow",
                "BigQuery",
                "Dataproc",
                "BigQuery",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-customerdata"],
            "business_unit": "SoftwareSolutions",
        },
        "CloudServiceTrustPlatform": {
            "description": "Platform to demonstrate and manage trust and compliance for the SaaS offering, addressing security and regulatory requirements.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-prod", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "AIHelpdeskChatbot": {
            "description": "AI-powered chatbot to provide automated customer support and answer common helpdesk queries.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "just_started",
            "services": [
                "VertexAI",
                "DialogFlow",
                "VertexAI",
                "VertexAI",
                "CloudFunctions",
                "Firestore",
                "ApiGateway",
                "CloudLogging",
            ],
            "stages": ["softwaresolutions-dev"],
            "business_unit": "SoftwareSolutions",
        },

        # Machine Learning Center of Excellence Projects
        "CentralizedFeatureRepository": {
            "description": "Centralized repository to store, manage, and share features for machine learning models across the organization.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "VertexAI",
                "CloudStorage",
                "Dataflow",
                "Dataflow",
                "BigQuery",
                "BigQuery",
                "CloudLogging",
            ],
            "stages": ["ml-featurestore"],
            "business_unit": "MachineLearning",
        },
        "ModelDeploymentPipeline": {
            "description": "Automated pipeline for deploying and managing machine learning models to production environments.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "VertexAI",
                "VertexAI",
                "CloudStorage",
                "Firestore",
                "CloudScheduler",
                "CloudLogging",
            ],
            "stages": ["ml-staging", "ml-prod"],
            "business_unit": "MachineLearning",
        },
        "SharedTrainingCompute": {
            "description": "Shared, scalable compute infrastructure for machine learning training workloads across different teams.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "VertexAI",
                "ComputeEngine",
                "PersistentDisk",
                "CloudStorage",
                "CloudMonitoring",
                "ComputeEngine",
                "CloudLogging",
            ],
            "stages": ["ml-staging"],
            "business_unit": "MachineLearning",
        },
        "RealTimeAnomalyDetection": {
            "description": "Real-time anomaly detection system to identify and alert on anomalies in data streams and system behavior.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "VertexAI",
                "VertexAI",
                "CloudStorage",
                "Pub/Sub",
                "Pub/Sub",
                "Looker",
                "CloudLogging",
            ],
            "stages": ["ml-prod", "ml-staging"],
            "business_unit": "MachineLearning",
        },
        "GenAIModelHub": {
            "description": "Centralized hub for managing, deploying, and accessing generative AI models across the organization.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "growing",
            "services": [
                "VertexAI",
                "ComputeEngine",
                "CloudRun",
                "ApiGateway",
                "CloudCDN",
                "CloudArmor",
                "ComputeEngine",
                "VertexAI",
                "CloudLogging",
            ],
            "stages": ["ml-prod"],
            "business_unit": "MachineLearning",
        },
        "MLOpsAutomationFramework": {
            "description": "Framework and tools for automating machine learning operations (MLOps), including model training, deployment, and monitoring.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "steady_state",
            "services": [
                "CloudScheduler",
                "Pub/Sub",
                "CloudBuild",
                "CloudBuild",
                "CloudBuild",
                "Pub/Sub",
                "Pub/Sub",
                "CloudLogging",
            ],
            "stages": ["ml-staging", "ml-prod"],
            "business_unit": "MachineLearning",
        },
        "MLSandboxEnvironment": {
            "description": "Isolated sandbox environment for data scientists and ML engineers to experiment, prototype, and develop ML solutions.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "just_started",
            "services": [
                "VertexAI",
                "ComputeEngine",
                "CloudStorage",
                "Firestore",
                "Looker",
                "CloudLogging",
            ],
            "stages": ["sandbox-central"],
            "business_unit": "MachineLearning",
        },

        # Core/Shared Services/Security/Compliance Projects
        "ThreatDetectionCenter": {
            "description": "Centralized threat detection and incident response center for proactive security monitoring and alerting.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
            ],
            "stages": ["security"],
            "business_unit": "Core",
        },
        "EnterpriseLoggingService": {
            "description": "Centralized logging service for collecting, storing, and analyzing logs from across the entire GCP environment.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudLogging",
                "Pub/Sub",
                "CloudStorage",
                "CloudStorage",
                "CloudLogging",
                "VPC",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "IdentityLifecycleManagement": {
            "description": "Service for managing the lifecycle of user identities and access across the organization's GCP footprint.",
            "use_case": "Security",
            "lifecycle": "steady_state",
            "services": [
                "IAM",
                "IAM",
                "KeyManagementService",
                "SecretManager",
                "SecurityCommandCenter",
            ],
            "stages": ["security"],
            "business_unit": "Core",
        },
        "CorporateNetworkProtection": {
            "description": "Comprehensive network security infrastructure to protect the organization's cloud and on-premises networks.",
            "use_case": "Security",
            "lifecycle": "steady_state",
            "services": [
                "VPC",
                "CloudArmor",
                "CloudArmor",
                "CloudArmor",
                "CloudDNS",
                "CloudInterconnect",
            ],
            "stages": ["security"],
            "business_unit": "Core",
        },
        "CloudCostOptimizationProgram": {
            "description": "Program dedicated to continuously monitor and optimize cloud spending, ensuring cost efficiency across all GCP projects.",
            "use_case": "Management & Governance",
            "lifecycle": "steady_state",
            "services": [
                "CloudBilling",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "CentralizedBackupService": {
            "description": "Centralized service providing backup and recovery for critical data and systems across the organization's GCP environment.",
            "use_case": "Storage",
            "lifecycle": "steady_state",
            "services": [
                "CloudStorage",
                "CloudStorage",
                "PersistentDisk",
                "CloudSQL",
                "CloudStorage",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "AutomatedPatchManagement": {
            "description": "Automated system for patching operating systems and applications across the organization's Compute Engine instances and servers.",
            "use_case": "Management & Governance",
            "lifecycle": "steady_state",
            "services": [
                "CloudMonitoring",
                "SecurityCommandCenter",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "InfrastructureVulnerabilityScanner": {
            "description": "Automated vulnerability scanning service to identify and report security vulnerabilities in the organization's cloud infrastructure.",
            "use_case": "Security",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudMonitoring",
                "ComputeEngine",
                "CloudLogging",
            ],
            "stages": ["security"],
            "business_unit": "Core",
        },
        "ComplianceReportingEngine": {
            "description": "Engine to automate the generation of compliance reports and dashboards for various regulatory frameworks.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "SecurityCommandCenter",
                "CloudLogging",
                "CloudLogging",
                "BigQuery",
                "Looker",
            ],
            "stages": ["compliance"],
            "business_unit": "Core",
        },
        "DisasterRecoveryDrills": {
            "description": "Orchestration and execution of disaster recovery drills to test and improve the organization's DR capabilities.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine",
                "CloudSQL",
                "CloudDNS",
                "CloudLogging",
                "CloudLogging",
                "ComputeEngine",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "CentralizedMonitoringDashboards": {
            "description": "Centralized monitoring dashboards providing a unified view of the health and performance of the organization's GCP environment.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudMonitoring",
                "ManagedGrafana",
                "Looker",
                "CloudLogging",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "InfraPipelineOrchestrator": {
            "description": "Centralized infrastructure pipeline orchestrator for automating the deployment and management of GCP infrastructure.",
            "use_case": "Management & Governance",
            "lifecycle": "steady_state",
            "services": [
                "CloudBuild",
                "CloudBuild",
                "CloudBuild",
                "DeploymentManager",
                "CloudMonitoring",
                "CloudLogging",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "EnterpriseDNSPlatform": {
            "description": "Enterprise-grade DNS platform providing reliable and scalable DNS services for the organization.",
            "use_case": "Networking",
            "lifecycle": "steady_state",
            "services": [
                "CloudDNS",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "CrossAccountBackupService": {
            "description": "Cross-project backup service enabling centralized backup and recovery management across multiple GCP projects.",
            "use_case": "Storage",
            "lifecycle": "steady_state",
            "services": [
                "CloudStorage",
                "CloudStorage",
                "CloudStorage",
                "CloudLogging",
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "SharedServicesDevSandbox": {
            "description": "Centralized sandbox environment for the Shared Services team to develop and test new infrastructure and automation.",
            "use_case": "Management & Governance",
            "lifecycle": "just_started",
            "services": [
                "ComputeEngine",
                "CloudFunctions",
                "CloudStorage",
                "CloudLogging",
            ],
            "stages": ["sandbox-central"],
            "business_unit": "Core",
        },

        # Enterprise Data Platform Projects
        "GlobalDataLakehouse": {
            "description": "Enterprise-wide data lakehouse platform integrating structured and unstructured data across all business units, with centralized governance, ML-ready datasets, and self-service analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "CloudStorage", "Dataflow", "BigQuery", "Dataflow", "Dataproc", "BigQuery",
                "Looker", "CloudFunctions", "CloudScheduler", "CloudLogging",
                "IAM", "KeyManagementService", "CloudLogging"
            ],
            "stages": ["shared-services", "ml-featurestore"],
            "business_unit": "Core",
        },
        "MultiRegionStreamingDataPipeline": {
            "description": "Global, fault-tolerant streaming data pipeline with multi-region replication, handling 10+ TB daily across 5 continents with sub-second latency requirements.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "Pub/Sub", "Pub/Sub", "Pub/Sub", "CloudStorage",
                "CloudFunctions", "Firestore", "Firestore", "CloudCDN", "CloudDNS",
                "CloudLogging", "Pub/Sub", "Pub/Sub", "CloudMonitoring"
            ],
            "stages": ["shared-services", "supplychain-analytics", "manufacturing-iot"],
            "business_unit": "SupplyChain",
        },
        "RegulatoryReportingDataWarehouse": {
            "description": "Centralized regulatory reporting platform integrating financial, risk, and compliance data with point-in-time recovery and full audit trails for financial regulations.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "BigQuery", "CloudStorage", "Dataflow", "BigQuery", "Looker",
                "CloudFunctions", "CloudScheduler", "CloudLogging", "CloudLogging",
                "CloudStorage", "KeyManagementService", "SecurityCommandCenter", "SecurityCommandCenter"
            ],
            "stages": ["compliance", "pharma-prod"],
            "business_unit": "Pharma",
        },

        # Global Customer-Facing Applications
        "OmniChannelCustomerExperience": {
            "description": "Global, multi-channel customer experience platform handling web, mobile, in-store, and call center interactions with a unified customer view and personalization.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "ComputeEngine", "CloudRun", "CloudSQL", "Firestore", "Memorystore", "CloudFunctions",
                "ApiGateway", "CloudCDN", "CloudDNS", "CloudStorage", "Pub/Sub", "Pub/Sub",
                "IAM", "CloudLogging", "CloudTrace", "CloudArmor"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "GlobalECommerceInfrastructure": {
            "description": "High-volume, global e-commerce platform handling millions of transactions daily with 99.99% availability across multiple regions and dynamic scaling during peak seasons.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine", "CloudSQL", "Firestore", "Memorystore", "CloudCDN",
                "CloudDNS", "CloudStorage", "CloudRun", "Pub/Sub", "Pub/Sub", "ApiGateway",
                "CloudFunctions", "CloudLogging", "CloudMonitoring", "CloudArmor",
                "CloudArmor", "IAM", "KeyManagementService"
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "MultiLanguageContentPlatform": {
            "description": "Enterprise content management platform supporting 40+ languages with distributed authoring, automated translation workflows, and global content delivery.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine", "CloudSQL", "CloudStorage", "CloudCDN", "CloudFunctions", "Pub/Sub",
                "Memorystore", "VertexAI", "CloudLogging", "VertexAI",
                "CloudScheduler", "IAM", "IAM"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },

        # AI/ML Enterprise Systems
        "EnterpriseLLMPlatform": {
            "description": "Enterprise-wide generative AI platform with fine-tuned large language models, specialized vertical models, and secure enterprise knowledge integration.",
            "use_case": "Generative AI and LLMs",
            "lifecycle": "growing",
            "services": [
                "VertexAI", "VertexAI", "VertexAI", "CloudStorage",
                "CloudFunctions", "Filestore", "ApiGateway", "CloudCDN", "ComputeEngine",
                "SecretManager", "CloudLogging", "KeyManagementService"
            ],
            "stages": ["ml-prod", "ml-staging"],
            "business_unit": "MachineLearning",
        },
        "VideoAnalyticsSecuritySystem": {
            "description": "Enterprise video surveillance analytics system processing feeds from 10,000+ cameras with real-time object detection, anomaly detection, and secure retention.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "VertexAI", "Pub/Sub", "Pub/Sub", "CloudStorage",
                "CloudFunctions", "Firestore", "ComputeEngine", "CloudRun", "VertexAI",
                "CloudLogging", "IAM", "KeyManagementService", "CloudMonitoring"
            ],
            "stages": ["security", "ml-prod"],
            "business_unit": "Security",
        },
        "PredictiveMaintenanceSystem": {
            "description": "Industrial-scale predictive maintenance system processing terabytes of sensor data daily from 50,000+ connected devices to forecast equipment failures.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "IoT", "IoTAnalytics", "Pub/Sub", "CloudStorage",
                "VertexAI", "CloudFunctions", "Firestore", "Pub/Sub", "BigQuery",
                "Looker", "CloudLogging", "Dataproc"
            ],
            "stages": ["manufacturing-iot", "manufacturing-prod", "ml-prod"],
            "business_unit": "Manufacturing",
        },

        # IoT and Edge Computing
        "SmartFactoryIoTPlatform": {
            "description": "Comprehensive smart factory platform connecting 100,000+ industrial sensors and controllers with real-time monitoring, digital twins, and predictive capabilities.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "IoT", "IoTSiteWise", "Pub/Sub", "BigQuery",
                "CloudStorage", "CloudFunctions", "Firestore", "Pub/Sub", "VertexAI",
                "CloudLogging", "Looker", "ComputeEngine", "GKE"
            ],
            "stages": ["manufacturing-iot", "manufacturing-prod", "manufacturing-analytics"],
            "business_unit": "Manufacturing",
        },
        "ConnectedAircraftAnalytics": {
            "description": "Aviation telematics platform processing in-flight data from 500+ aircraft, with edge computing capabilities, satellite connectivity, and predictive analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "IoT", "IoTAnalytics", "CloudStorage", "Pub/Sub",
                "Dataflow", "BigQuery", "Dataproc", "CloudFunctions", "VertexAI",
                "CloudLogging", "Looker", "BigQuery"
            ],
            "stages": ["aviation-iot", "aviation-analytics"],
            "business_unit": "Aviation",
        },
        "GlobalLogisticsTrackingNetwork": {
            "description": "Worldwide logistics tracking system monitoring millions of shipments in real-time across global supply chains with predictive ETAs and disruption management.",
            "use_case": "Enterprise Integration",
            "lifecycle": "steady_state",
            "services": [
                "IoT", "Pub/Sub", "CloudStorage", "Firestore", "CloudFunctions",
                "ApiGateway", "CloudCDN", "ComputeEngine", "Pub/Sub",
                "CloudScheduler", "CloudLogging", "Dataproc"
            ],
            "stages": ["supplychain-logistics", "supplychain-prod"],
            "business_unit": "SupplyChain",
        },

        # Financial Systems
        "GlobalPaymentProcessingPlatform": {
            "description": "High-throughput payment processing platform handling millions of transactions daily across 30+ countries with stringent security and compliance requirements.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine", "CloudSQL", "Firestore", "Memorystore", "CloudFunctions",
                "CloudScheduler", "Pub/Sub", "KeyManagementService", "CloudHSM", "CloudArmor",
                "CloudLogging", "CloudLogging", "SecurityCommandCenter"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "EnterpriseFinancialReportingSystem": {
            "description": "Consolidated financial reporting platform integrating data from 50+ global subsidiaries with multi-currency support, complex allocations, and regulatory compliance.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "ComputeEngine", "CloudSQL", "CloudStorage", "CloudFunctions", "CloudScheduler",
                "Looker", "Dataflow", "BigQuery", "CloudLogging",
                "KeyManagementService", "SecurityCommandCenter", "CloudLogging"
            ],
            "stages": ["softwaresolutions-prod", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "TaxCalculationEngine": {
            "description": "Global tax calculation engine with coverage for 120+ countries, handling millions of complex tax determinations daily with automatic regulatory updates.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "ComputeEngine", "CloudSQL", "CloudFunctions", "ApiGateway", "CloudStorage",
                "Firestore", "CloudCDN", "CloudRun", "CloudLogging",
                "CloudLogging", "KeyManagementService", "SecurityCommandCenter"
            ],
            "stages": ["supplychain-prod", "compliance"],
            "business_unit": "SupplyChain",
        },

        # Enterprise Security Solutions
        "EnterpriseSecurityOperationsCenter": {
            "description": "24/7 global security operations center monitoring all enterprise systems with threat intelligence integration, automated incident response, and compliance reporting.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityCommandCenter", "SecurityCommandCenter", "SecurityCommandCenter", "SecurityCommandCenter",
                "SecurityCommandCenter", "CloudLogging", "CloudLogging", "CloudFunctions",
                "Pub/Sub", "CloudScheduler", "Pub/Sub", "KeyManagementService"
            ],
            "stages": ["security", "compliance"],
            "business_unit": "Core",
        },
        "DataPrivacyCompliancePlatform": {
            "description": "Enterprise platform for managing data privacy compliance across GDPR, CCPA, and other regulations with data discovery, consent management, and DSR handling.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "growing",
            "services": [
                "SecurityCommandCenter", "Dataflow", "BigQuery", "CloudStorage", "CloudFunctions",
                "CloudScheduler", "Firestore", "ApiGateway", "CloudLogging",
                "CloudLogging", "KeyManagementService", "SecurityCommandCenter", "SecurityCommandCenter"
            ],
            "stages": ["security", "compliance", "softwaresolutions-customerdata"],
            "business_unit": "Core",
        },
        "EnterpriseCryptoKeyManagement": {
            "description": "Global cryptographic key management service handling millions of keys across multiple regions with HSM backing, strict compliance controls, and automated rotation.",
            "use_case": "Security",
            "lifecycle": "steady_state",
            "services": [
                "KeyManagementService", "CloudHSM", "SecretManager", "CloudFunctions",
                "Firestore", "CloudLogging", "CloudLogging", "Pub/Sub",
                "Pub/Sub", "IAM"
            ],
            "stages": ["security", "shared-services"],
            "business_unit": "Core",
        },

        # Media Processing & Delivery
        "GlobalMediaProcessingPlatform": {
            "description": "Media processing platform handling millions of videos with automated transcoding, content moderation, subtitle generation, and global delivery.",
            "use_case": "Enterprise Applications",
            "lifecycle": "growing",
            "services": [
                "MediaConvert", "MediaPackage", "CloudStorage", "CloudCDN",
                "CloudFunctions", "CloudScheduler", "Pub/Sub", "VertexAI",
                "VertexAI", "CloudLogging", "Elemental"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "BroadcastMediaDistribution": {
            "description": "Broadcast-grade media distribution network handling live and on-demand content for global audiences with multi-region redundancy and DRM protection.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "MediaLive", "MediaConnect", "MediaPackage", "CloudStorage",
                "CloudCDN", "CloudDNS", "CloudArmor", "CloudArmor",
                "CloudLogging", "CloudFunctions", "ApiGateway"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "EnterpriseDigitalAssetManagement": {
            "description": "Centralized digital asset management platform for 100+ million assets with AI-powered tagging, version control, rights management, and global distribution.",
            "use_case": "Enterprise Applications",
            "lifecycle": "growing",
            "services": [
                "CloudStorage", "Firestore", "ElasticSearch", "VertexAI",
                "VertexAI", "CloudFunctions", "ComputeEngine", "CloudRun", "CloudCDN",
                "CloudLogging", "CloudScheduler", "Pub/Sub"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-customerdata"],
            "business_unit": "SoftwareSolutions",
        },

        # Healthcare Systems
        "ClinicalTrialsManagementPlatform": {
            "description": "Global platform for managing multi-center clinical trials with patient engagement, real-time monitoring, regulatory compliance, and data security.",
            "use_case": "Enterprise Applications",
            "lifecycle": "growing",
            "services": [
                "ComputeEngine", "CloudSQL", "Firestore", "CloudStorage", "CloudFunctions",
                "ApiGateway", "IAM", "CloudCDN", "CloudLogging",
                "KeyManagementService", "CloudLogging", "SecurityCommandCenter", "SecurityCommandCenter"
            ],
            "stages": ["pharma-prod", "pharma-research", "compliance"],
            "business_unit": "Pharma",
        },
        "HealthcareDataInteroperabilityHub": {
            "description": "Interoperability platform connecting healthcare systems via FHIR, HL7, DICOM with real-time transforms, API management, and secure patient data exchange.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "ApiGateway", "ApiGateway", "CloudFunctions", "Firestore",
                "ComputeEngine", "CloudRun", "Pub/Sub", "Pub/Sub", "CloudStorage", "ElasticSearch",
                "CloudLogging", "KeyManagementService", "CloudScheduler", "HealthLake"
            ],
            "stages": ["pharma-prod", "pharma-research"],
            "business_unit": "Pharma",
        },
        "MedicalImageProcessingPlatform": {
            "description": "High-performance platform for processing and analyzing medical imaging data (CT, MRI, ultrasound) with AI diagnosis assistance and research capabilities.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "ComputeEngine", "CloudStorage", "Filestore", "VertexAI", "VertexAI",
                "CloudFunctions", "BatchService", "Firestore", "CloudLogging",
                "Pub/Sub", "Pub/Sub", "KeyManagementService", "CloudCDN"
            ],
            "stages": ["pharma-research", "ml-prod"],
            "business_unit": "Pharma",
        },

        # Geospatial Solutions
        "GeospatialAnalyticsPlatform": {
            "description": "Enterprise geospatial analytics platform processing satellite, drone, and sensor imagery for agriculture, infrastructure monitoring, and environmental analysis.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "CloudStorage", "ComputeEngine", "GKE", "CloudFunctions", "VertexAI",
                "BigQuery", "Looker", "CloudLogging", "CloudScheduler",
                "BatchService", "Dataflow", "Location"
            ],
            "stages": ["ml-prod", "supplychain-analytics"],
            "business_unit": "MachineLearning",
        },
        "FleetManagementTelematics": {
            "description": "Real-time fleet management system monitoring 10,000+ vehicles with route optimization, predictive maintenance, and driver behavior analytics.",
            "use_case": "Enterprise Integration",
            "lifecycle": "steady_state",
            "services": [
                "IoT", "Pub/Sub", "BigQuery", "CloudStorage",
                "CloudFunctions", "Firestore", "Pub/Sub", "ApiGateway", "CloudLogging",
                "Looker", "Dataproc", "Location"
            ],
            "stages": ["supplychain-logistics", "manufacturing-iot"],
            "business_unit": "SupplyChain",
        },
        "DisasterResponseCoordinationSystem": {
            "description": "Multi-agency disaster response coordination platform with real-time resource tracking, geospatial analytics, and field communication capabilities.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "Location", "ApiGateway", "CloudFunctions", "Firestore",
                "IoT", "Pub/Sub", "CloudStorage", "CloudCDN", "CloudLogging",
                "KeyManagementService", "ElasticSearch", "CloudScheduler"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },

        # Enterprise DevOps Platforms
        "GlobalCICDPlatform": {
            "description": "Enterprise-wide CI/CD platform handling 5000+ daily builds across 200+ teams with automated testing, security scanning, and global artifact distribution.",
            "use_case": "Developer Tools",
            "lifecycle": "peak_and_plateau",
            "services": [
                "CloudBuild", "CloudBuild", "CloudBuild", "ComputeEngine",
                "CloudRun", "GKE", "CloudStorage", "CloudCDN", "CloudFunctions",
                "CloudLogging", "CloudLogging", "KeyManagementService", "Pub/Sub", "Pub/Sub"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "MultiCloudInfrastructureOrchestration": {
            "description": "Infrastructure-as-Code platform managing resources across GCP, Azure, AWS with centralized governance, drift detection, and compliance enforcement.",
            "use_case": "Management & Governance",
            "lifecycle": "growing",
            "services": [
                "DeploymentManager", "CloudMonitoring", "CloudFunctions", "Firestore",
                "CloudStorage", "Pub/Sub", "Pub/Sub", "Pub/Sub", "CloudLogging",
                "CloudLogging", "SecurityCommandCenter", "CloudBuild"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "EnterpriseServiceMesh": {
            "description": "Global service mesh controlling 1000+ microservices across multiple clusters with traffic management, security, observability, and chaos engineering capabilities.",
            "use_case": "Management & Governance",
            "lifecycle": "growing",
            "services": [
                "GKE", "ComputeEngine", "CloudFunctions", "AppMesh", "CloudTrace",
                "CloudLogging", "CloudMonitoring", "VPC", "CloudDNS",
                "Certificate Manager", "IAM", "ElasticSearch"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        }
    }
}
