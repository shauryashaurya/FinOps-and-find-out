# config.py
# Configuration for AWS Cost and Usage Report (CUR) simulation.
# This file defines AWS services, pricing models, example projects,
# and organizational structure to generate realistic, CUR-like data for cost analysis and optimization scenarios.
# Note: AWS pricing and service availability can vary significantly by region.
# In actual CUR data, the 'region' attribute is a key field within each usage record,
# indicating the AWS region where the resource or usage originated.
# AWS CUR is generally provided at an account level, meaning a single CUR file will contain
# cost and usage data for all regions used by that AWS account, not separate files per region.

AWS_REGIONS = [
    "us-east-1",  # US East (N. Virginia)
    "us-east-2",  # US East (Ohio)
    "us-west-1",  # US West (N. California)
    "us-west-2",  # US West (Oregon)
    "ap-south-1",  # Asia Pacific (Mumbai)
    "ap-southeast-1",  # Asia Pacific (Singapore)
    "ap-southeast-2",  # Asia Pacific (Sydney)
    "ap-northeast-1",  # Asia Pacific (Tokyo)
    "ap-northeast-2",  # Asia Pacific (Seoul)
    "eu-central-1",  # Europe (Frankfurt)
    "eu-west-1",  # Europe (Ireland)
    "eu-west-2",  # Europe (London)
    "eu-west-3",  # Europe (Paris)
    "ca-central-1",  # Canada (Central)
    "sa-east-1",  # South America (Sao Paulo)
    "af-south-1",  # Africa (Cape Town)
    "me-south-1",  # Middle East (Bahrain)
    "ap-east-1",  # Asia Pacific (Hong Kong)
    "eu-north-1",  # Europe (Stockholm)
    "eu-south-1",  # Europe (Milan)
    "us-gov-east-1",  # AWS GovCloud (US-East) - Added for diversity
    "us-gov-west-1",  # AWS GovCloud (US-West) - Added for diversity
]

REGIONAL_COST_FACTORS = {
    "us-east-1": 1.0,
    "us-east-2": 1.01,
    "us-west-1": 1.02,
    "us-west-2": 1.015,
    "ap-south-1": 1.05,
    "ap-southeast-1": 1.03,
    "ap-southeast-2": 1.04,
    "ap-northeast-1": 1.035,
    "ap-northeast-2": 1.03,
    "eu-central-1": 1.025,
    "eu-west-1": 1.02,
    "eu-west-2": 1.03,
    "eu-west-3": 1.022,
    "ca-central-1": 1.025,
    "sa-east-1": 1.04,
    "af-south-1": 1.06,
    "me-south-1": 1.055,
    "ap-east-1": 1.045,
    "eu-north-1": 1.03,
    "eu-south-1": 1.028,
    "us-gov-east-1": 1.1,
    "us-gov-west-1": 1.12
}


AWS_SERVICES = {
    "Analytics": {
        "Athena": {
            "base_rate": 0.005,
            "operations": ["QueryOperations"],
            "price_range": (0.001, 0.01),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["DataScanned-GB"],
        },
        "DataBrew": {
            "base_rate": 4.8,
            "operations": ["DataBrewInteractiveSessions"],
            "price_range": (3.0, 6.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["DataBrewSessionHours"],
        },
        "DataSync": {
            "base_rate": 0.0125,
            "operations": ["DataTransferOperations"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["DataSync-DataProcessed-GB"],
        },
        "EMR": {
            "base_rate": 0.05,
            "instance_types": ["m5.xlarge", "m5.2xlarge", "r5.xlarge", "r5.2xlarge"],
            "operations": [
                "ClusterOperations",
                "JobOperations",
                "ManagementOperations",
            ],
            "price_range": (0.01, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["InstanceHours", "EMRClusterHours"],
        },
        "Glue": {
            "base_rate": 0.44,
            "operations": ["ETLJobOperations", "DataCatalogOperations"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "DPU-Hours",
            "usage_types": ["DPU-Hours", "GlueDataCatalogStorage-GB-Month"],
        },
        "KinesisDataAnalytics": {
            "base_rate": 0.11,
            "operations": ["DataAnalyticsOperations"],
            "price_range": (0.05, 0.2),
            "pricing_model": "on_demand",
            "unit": "SPU-Hrs",
            "usage_types": ["KinesisDataAnalytics-SPU-Hours"],
        },
        "KinesisDataStreams": {
            "base_rate": 0.021,
            "operations": ["DataStreamingOperations"],
            "price_range": (0.01, 0.05),
            "pricing_model": "on_demand",
            "unit": "Shard-Hrs",
            "usage_types": [
                "KinesisDataStreams-ShardHours",
                "KinesisDataStreams-PUT-GB",
            ],
        },
        "LakeFormation": {
            "base_rate": 0.025,
            "operations": ["GovernanceOperations", "MetadataOperations"],
            "price_range": (0.01, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": [
                "LakeFormationGovernedTableStorage-GB-Month",
                "LakeFormationRequests",
            ],
        },
        "MSK": {
            "base_rate": 0.2,
            "instance_types": ["kafka.m5.large", "kafka.m5.xlarge", "kafka.m5.2xlarge"],
            "operations": ["KafkaClusterOperations", "StorageUsage", "DataTransfer"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "MSK-BrokerHours",
                "MSK-Storage-GB-Month",
                "DataTransfer-Out-MSK",
            ],
        },
        "QuickSight": {
            "base_rate": 12.0,
            "operations": ["DashboardUsage", "SPICEUsage"],
            "price_range": (5.0, 25.0),
            "pricing_model": "monthly",
            "unit": "Months",
            "usage_types": ["UserMonths", "SPICE-GB"],
        },
        "Redshift": {
            "base_rate": 0.25,
            "instance_types": ["dc2.large", "dc2.8xlarge", "ra3.xlplus", "ra3.4xlarge"],
            "operations": [
                "ClusterOperations",
                "QueryOperations",
                "StorageUsage",
                "DataTransfer",
                "SpectrumOperations",
            ],
            "price_range": (0.1, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "NodeHours",
                "Redshift:Storage-GB",
                "DataTransfer-Out",
                "DataTransfer-In",
                "Redshift:Spectrum-DataScanned-GB",
            ],
        },
    },
    "Application Integration": {
        "APIGateway": {
            "base_rate": 3.5,
            "operations": ["APIOperations", "DataTransfer"],
            "price_range": (1.0, 5.0),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": ["APICalls", "APIGatewayDataTransfer-Out"],
        },
        "AppSync": {
            "base_rate": 4.0,
            "operations": ["GraphQLOperations", "RealtimeDataOperations"],
            "price_range": (1.0, 6.0),
            "pricing_model": "consumption-based",
            "unit": "Million Operations",
            "usage_types": ["GraphQLQueriesAndDataModifications", "RealtimeUpdates"],
        },
        "Cognito": {
            "base_rate": 0.0055,
            "operations": ["UserManagementOperations", "FunctionInvocations"],
            "price_range": (0.001, 0.01),
            "pricing_model": "monthly",
            "unit": "Users-Month",
            "usage_types": ["Cognito-MAU-Users", "Cognito-Lambda-Invocations"],
        },
        "EventBridge": {
            "base_rate": 0.01,
            "operations": ["EventOperations"],
            "price_range": (0.005, 0.05),
            "pricing_model": "on_demand",
            "unit": "Events",
            "usage_types": ["EventsPublished"],
        },
        "MQ": {
            "base_rate": 0.15,
            "instance_types": ["mq.m5.large", "mq.m5.xlarge", "mq.m5.2xlarge"],
            "operations": ["MessageBrokerOperations", "StorageUsage"],
            "price_range": (0.1, 0.5),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["MQ-BrokerHours", "MQ-Storage-GB-Month"],
        },
        "SNS": {
            "base_rate": 0.5,
            "operations": ["MessageOperations", "DataTransfer"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": [
                "Requests",
                "DataTransfer-Out",
                "SNSDataTransfer-Out-Region",
            ],
        },
        "SQS": {
            "base_rate": 0.4,
            "operations": ["MessageOperations", "DataTransfer"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": ["Requests", "SQSDataTransfer-Out-Region"],
        },
        "StepFunctions": {
            "base_rate": 2.5e-05,
            "operations": ["WorkflowOperations"],
            "price_range": (1e-05, 0.0001),
            "pricing_model": "on_demand",
            "unit": "Transitions",
            "usage_types": ["StateTransitions"],
        },
    },
    "Compute": {
        "AutoScaling": {
            "base_rate": 0.005,
            "operations": ["ManageGroup"],
            "price_range": (0.001, 0.01),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["AutoScalingGroupHours"],
        },
        "EC2": {
            "base_rate": 0.05,
            "instance_types": [
                "t2.micro",
                "t2.small",
                "t2.medium",
                "t2.large",
                "m5.large",
                "m5.xlarge",
                "m5.2xlarge",
                "m5.4xlarge",
                "c5.large",
                "c5.xlarge",
                "c5.2xlarge",
                "c5.4xlarge",
                "r5.large",
                "r5.xlarge",
                "r5.2xlarge",
                "r5.4xlarge",
            ],
            "operations": ["RunInstances", "EC2-DataTransfer"],
            "price_range": (0.01, 5.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "BoxUsage",
                "DataTransfer-Out",
                "DataTransfer-In",
                "EBS:VolumeUsage.gp2",
            ],
        },
        "ECS": {
            "base_rate": 0.04,
            "operations": ["RunTask", "StartTask"],
            "price_range": (0.01, 0.2),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["ECS-Fargate-vCPU", "ECS-Fargate-Memory"],
        },
        "ElasticBeanstalk": {
            "base_rate": 0.01,
            "operations": ["ManageApplication"],
            "price_range": (0.005, 0.05),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["ApplicationHours"],
        },
        "Lambda": {
            "base_rate": 1.667e-05,
            "operations": ["InvokeFunction"],
            "price_range": (1e-07, 0.0001),
            "pricing_model": "on_demand",
            "unit": "GB-Seconds",
            "usage_types": ["Duration", "Requests", "GB-Seconds"],
        },
    },
    "Database": {
        "DynamoDB": {
            "base_rate": 0.000125,
            "operations": ["DataOperations", "StorageUsage", "GlobalTableOperations"],
            "price_range": (1e-05, 0.01),
            "pricing_model": "on_demand",
            "unit": "RequestUnits",
            "usage_types": [
                "WriteRequestUnits",
                "ReadRequestUnits",
                "Storage-GB",
                "DynamoDB:GlobalTableWriteRequestUnits",
                "DynamoDB:GlobalTableReadRequestUnits",
            ],
        },
        "ElastiCache": {
            "base_rate": 0.026,
            "instance_types": [
                "cache.t2.micro",
                "cache.t2.small",
                "cache.t2.medium",
                "cache.m5.large",
                "cache.m5.xlarge",
            ],
            "operations": ["CacheOperations", "DataTransfer", "BackupOperations"],
            "price_range": (0.01, 2.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "CacheNodeUsage",
                "DataTransfer-Out",
                "DataTransfer-In",
                "ElastiCache:BackupStorage-GB",
            ],
        },
        "RDS": {
            "base_rate": 0.025,
            "instance_types": [
                "db.t2.micro",
                "db.t2.small",
                "db.t2.medium",
                "db.m5.large",
                "db.m5.xlarge",
                "db.m5.2xlarge",
            ],
            "operations": [
                "DBOperations",
                "StorageUsage",
                "DataTransfer",
                "IOOperations",
                "BackupOperations",
            ],
            "price_range": (0.01, 2.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "DBInstanceUsage",
                "RDS:Storage-GB",
                "DataTransfer-Out",
                "DataTransfer-In",
                "IO-Requests",
                "RDS:BackupStorage-GB",
            ],
        },
        "Timestream": {
            "base_rate": 0.10,  # $0.10 per GB of data write
            "operations": [
                "WriteOperations",
                "ReadOperations",
                "StorageOperations"
            ],
            "price_range": (0.05, 0.30),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": [
                "TimestreamWrite-GB",
                "TimestreamRead-GB",
                "TimestreamStorage-MB-Month"
            ],
        },
    },
    "Developer Tools": {
        "CodePipeline": {
            "base_rate": 1.0,
            "operations": ["PipelineExecution", "StageExecution", "ActionExecution"],
            "price_range": (0.5, 2.0),
            "pricing_model": "on_demand",
            "unit": "Pipelines-Month",
            "usage_types": ["CodePipeline-ActivePipelines", "CodePipeline-Executions"],
        },
        "CodeBuild": {
            "base_rate": 0.005,
            "operations": ["BuildExecution", "BatchBuild"],
            "price_range": (0.001, 0.01),
            "pricing_model": "on_demand",
            "unit": "BuildMinute",
            "usage_types": ["CodeBuild-BuildMinutes", "CodeBuild-ComputeType"],
        },
        "CodeDeploy": {
            "base_rate": 0.02,
            "operations": ["DeploymentOperations", "InstanceDeployment"],
            "price_range": (0.01, 0.05),
            "pricing_model": "on_demand",
            "unit": "OnPremiseInstance",
            "usage_types": ["CodeDeploy-OnPremiseInstances"],
        },
    },
    "Machine Learning": {
        "Bedrock": {
            "base_rate": 0.0001,
            "operations": ["BedrockInferenceOperations"],
            "price_range": (1e-05, 0.001),
            "pricing_model": "on_demand",
            "unit": "Requests",
            "usage_types": ["BedrockInferenceRequests"],
        },
        "Comprehend": {
            "base_rate": 3.0,
            "operations": ["NLPProcessingOperations"],
            "price_range": (1.0, 5.0),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["Comprehend-ProcessedGB"],
        },
        "Lex": {
            "base_rate": 4.0,
            "operations": ["ChatbotOperations"],
            "price_range": (2.0, 6.0),
            "pricing_model": "on_demand",
            "unit": "1000Requests",
            "usage_types": ["Lex-VoiceRequest", "Lex-TextRequest"],
        },
        "Rekognition": {
            "base_rate": 1.0,
            "operations": ["ImageAnalysisOperations", "VideoAnalysisOperations"],
            "price_range": (0.5, 2.0),
            "pricing_model": "on_demand",
            "unit": "1000Images",
            "usage_types": [
                "Rekognition-ImageAnalysis-1000Images",
                "Rekognition-VideoAnalysis-Second",
            ],
        },
        "SageMaker": {
            "base_rate": 0.3,
            "instance_types": [
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.p2.xlarge",
            ],
            "operations": ["TrainingOperations"],
            "price_range": (0.1, 10.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["TrainingInstanceHours"],
        },
        "SageMakerFeatureStore": {
            "base_rate": 0.2,
            "operations": [
                "FeatureStoreOperations",
                "OnlineStorageOperations",
                "OfflineStorageOperations",
                "IngestionOperations",
            ],
            "price_range": (0.05, 0.5),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": [
                "FeatureStoreOnlineStorage-GB-Month",
                "FeatureStoreOfflineStorage-GB-Month",
                "FeatureStoreIngestionHours",
            ],
        },
        "SageMakerGroundTruth": {
            "base_rate": 0.08,
            "operations": ["LabelingOperations", "DataPreprocessingOperations"],
            "price_range": (0.02, 0.2),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["LabelingTaskHours", "DataTransformHours"],
        },
        "SageMakerInference": {
            "base_rate": 0.35,
            "instance_types": [
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.g4dn.xlarge",
            ],
            "operations": ["InferenceOperations", "EndpointOperations"],
            "price_range": (0.1, 12.0),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["InferenceInstanceHours"],
        },
        "SageMakerJumpStart": {
            "base_rate": 0.5,
            "operations": ["ModelAccessOperations"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "AccessUnit",
            "usage_types": ["SageMakerJumpStart-ModelAccess"],
        },
    },
    "Management & Governance": {
        "SystemsManager": {
            "base_rate": 2.0,
            "operations": [
                "InstanceManagementOperations",
                "AutomationOperations",
                "PatchManagementOperations",
                "InventoryOperations",
            ],
            "price_range": (1.0, 5.0),
            "pricing_model": "monthly",
            "unit": "Instances-Month",
            "usage_types": [
                "ManagedInstances-Month",
                "AutomationExecutions",
                "PatchManagerScans",
                "InventoryDataStorage-GB-Month",
            ],
        },
        # Corrected service name from "SystemsManager" to "CloudWatch" for logs
        "CloudWatch": {
            "base_rate": 2.5,
            "operations": ["LogOperations", "MetricOperations", "AlarmOperations"],
            "price_range": (0.5, 5.0),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": [
                "CloudWatchLogs-GB",
                "CloudWatchMetrics-StandardResolutionMetrics",
                "CloudWatchAlarms",
            ],
        },
        "CloudFormation": {
            "base_rate": 0.0,  # CloudFormation is free for the service itself
            "operations": ["StackOperations", "ChangeSetOperations"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Operations",
            "usage_types": ["CloudFormation-Operations"],
        },
        "CostExplorer": {
            "base_rate": 0.01,
            "operations": ["APIRequests", "ReportGeneration"],
            "price_range": (0.005, 0.02),
            "pricing_model": "on_demand",
            "unit": "APIRequest",
            "usage_types": ["CostExplorer-APIRequest", "CostExplorer-Report"],
        },
    },
    "Networking": {
        "CloudFront": {
            "base_rate": 0.085,
            "operations": ["ContentDelivery", "Invalidation", "OriginShieldOperations"],
            "price_range": (0.01, 0.2),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": [
                "DataTransfer-Out",
                "DataTransfer-In",
                "Requests-HTTP",
                "Requests-HTTPS",
                "InvalidationRequests",
                "CloudFront:OriginShield-GB",
            ],
        },
        "DirectConnect": {
            "base_rate": 0.02,
            "operations": ["DXPortOperations", "DataTransfer"],
            "price_range": (0.01, 0.5),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": ["PortHours", "DataTransfer-Out-DX"],
        },
        "NetworkFirewall": {
            "base_rate": 0.396,
            "operations": [
                "FirewallRuleOperations",
                "NetworkFirewallOperations",
                "TrafficInspectionOperations",
            ],
            "price_range": (0.1, 1.0),
            "pricing_model": "hourly",
            "unit": "Hrs",
            "usage_types": [
                "FirewallEndpoints-Hours",
                "FirewallRuleGroups-RuleCount",
                "StatefulRuleEngine-GBProcessed",
                "StatelessRuleEngine-GBProcessed",
            ],
        },
        "Route53": {
            "base_rate": 0.5,
            "operations": ["DNSOperations", "ZoneManagement", "HealthCheckOperations"],
            "price_range": (0.1, 2.0),
            "pricing_model": "on_demand",
            "unit": "Months",
            "usage_types": ["HostedZoneMonths", "Queries", "HealthChecks"],
        },
        "VPC": {
            "base_rate": 0.01,
            "operations": [
                "EndpointOperations",
                "NATOperations",
                "DataTransfer",
                "VPNOperations",
            ],
            "price_range": (0.005, 0.1),
            "pricing_model": "on_demand",
            "unit": "Hrs",
            "usage_types": [
                "VPCEndpointHours",
                "NATGatewayHours",
                "DataProcessed-GB",
                "VPNConnectionHours",
                "VPNGatewayHours",
            ],
        },
    },
    "Observability": {
        "CloudTrail": {
            "base_rate": 2.0,
            "operations": ["AuditLoggingOperations"],
            "price_range": (0.5, 5.0),
            "pricing_model": "on_demand",
            "unit": "Events",
            "usage_types": ["CloudTrailEvents"],
        },
        # Corrected service name from "CloudWatchSynthetics" to "CloudWatchLogs"
        "CloudWatchLogs": {
            "base_rate": 2.5,  # Example rate, adjust as needed
            "operations": ["LogOperations"],
            "price_range": (0.5, 5.0),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": [
                "CloudWatchLogs-GB"
            ],  # Example Usage Type for CloudWatch Logs
        },
        "CloudWatchSynthetics": {
            "base_rate": 0.006,
            "operations": ["SyntheticMonitoringOperations"],
            "price_range": (0.002, 0.01),
            "pricing_model": "on_demand",
            "unit": "CanaryRuns",
            "usage_types": ["CloudWatchSynthetics-CanaryRuns"],
        },
        "KinesisDataFirehose": {
            "base_rate": 0.029,
            "operations": ["DataDeliveryOperations"],
            "price_range": (0.01, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["KinesisFirehoseDataIngested-GB"],
        },
        "ManagedGrafana": {
            "base_rate": 9.0,
            "operations": ["DashboardingOperations"],
            "price_range": (5.0, 15.0),
            "pricing_model": "monthly",
            "unit": "Users-Month",
            "usage_types": ["ManagedGrafana-ActiveUsers"],
        },
        "XRay": {
            "base_rate": 5.0,
            "operations": ["TracingOperations"],
            "price_range": (1.0, 10.0),
            "pricing_model": "on_demand",
            "unit": "Traces",
            "usage_types": ["TracesAnalyzed"],
        },
    },
    "Security": {
        "AuditManager": {
            "base_rate": 250.0,
            "operations": ["AuditAssessmentOperations", "EvidenceStorageOperations"],
            "price_range": (100.0, 500.0),
            "pricing_model": "monthly",
            "unit": "Months",
            "usage_types": [
                "AuditManagerAssessmentMonths",
                "AuditManagerEvidenceStorage-GB-Month",
            ],
        },
        "Config": {
            "base_rate": 2.0,
            "operations": ["ConfigurationTracking", "RuleEvaluations"],
            "price_range": (1.0, 5.0),
            "pricing_model": "on_demand",
            "unit": "Rules-Month",
            "usage_types": ["ConfigRulesActive", "ConfigRuleEvaluations"],
        },
        "GuardDuty": {
            "base_rate": 0.4,
            "operations": ["SecurityAnalysis", "MalwareScanOperations"],
            "price_range": (0.1, 1.0),
            "pricing_model": "on_demand",
            "unit": "GB",
            "usage_types": ["DataAnalyzed-GB", "GuardDutyMalwareScan-GB"],
        },
        "IAMAccessAnalyzer": {
            "base_rate": 10.0,
            "operations": ["AccessAnalysisOperations"],
            "price_range": (5.0, 20.0),
            "pricing_model": "monthly",
            "unit": "Months",
            "usage_types": ["AccessAnalyzerActiveAnalyzers"],
        },
        "IAMIdentityCenter": {
            "base_rate": 1.0,
            "operations": [
                "IdentityManagementOperations",
                "AccessManagementOperations",
            ],
            "price_range": (0.5, 2.0),
            "pricing_model": "monthly",
            "unit": "Users-Month",
            "usage_types": ["ActiveUsers-Month"],
        },
        "Inspector": {
            "base_rate": 2.0,
            "operations": ["VulnerabilityAssessmentOperations"],
            "price_range": (1.0, 4.0),
            "pricing_model": "on_demand",
            "unit": "Assessments",
            "usage_types": [
                "Inspector-AgentAssessment-Instances",
                "Inspector-AgentAssessment-Hosts",
            ],
        },
        "KMS": {
            "base_rate": 0.03,
            "operations": ["KeyManagementOperations", "EncryptionOperations"],
            "price_range": (0.01, 0.1),
            "pricing_model": "on_demand",
            "unit": "10000Requests",
            "usage_types": ["KMS-KeyUsage", "KMS-KeyStorage-Month"],
        },
        "SecurityHub": {
            "base_rate": 0.02,
            "operations": ["SecurityFindingsOperations"],
            "price_range": (0.01, 0.05),
            "pricing_model": "on_demand",
            "unit": "10000Findings",
            "usage_types": ["SecurityHub-FindingsIngested"],
        },
        "SecurityLake": {
            "base_rate": 0.025,
            "operations": ["SecurityDataLakeOperations", "QueryOperations"],
            "price_range": (0.01, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": ["SecurityLakeStorage-GB-Month", "SecurityLakeRequests"],
        },
        "ShieldAdvanced": {
            "base_rate": 3000.0,
            "operations": ["DDOSProtectionOperations", "DataTransfer"],
            "price_range": (2500.0, 3500.0),
            "pricing_model": "monthly",
            "unit": "Months",
            "usage_types": [
                "ShieldAdvanced-SubscriptionMonths",
                "ShieldAdvanced-DataTransfer-Out-Protected",
            ],
        },
        "WAF": {
            "base_rate": 5.0,
            "operations": [
                "WebRequestProcessing",
                "RuleManagement",
                "WAFv2RuleManagement",
            ],
            "price_range": (1.0, 10.0),
            "pricing_model": "on_demand",
            "unit": "Months",
            "usage_types": ["WAFRuleMonths", "Requests", "WAFv2RuleMonths"],
        },
        "SecretsManager": {
            "base_rate": 0.40,
            "operations": ["SecretStorage", "SecretAccess", "SecretRotation"],
            "price_range": (0.3, 0.5),
            "pricing_model": "on_demand",
            "unit": "Secret-Month",
            "usage_types": ["SecretsManager-Secret-Month", "SecretsManager-API-Requests"],
        },
        "IAM": {
            "base_rate": 0.0,  # IAM is free
            "operations": ["UserManagement", "RoleManagement", "PermissionManagement"],
            "price_range": (0.0, 0.0),
            "pricing_model": "free",
            "unit": "Operations",
            "usage_types": ["IAM-Operations"],
        },
    },
    "Storage": {
        "EBS": {
            "base_rate": 0.1,
            "operations": ["StorageOperations", "SnapshotOperations"],
            "price_range": (0.05, 0.5),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": [
                "EBS:VolumeUsage.gp2",
                "EBS:VolumeUsage.io1",
                "EBS:VolumeUsage.st1",
                "EBS:VolumeUsage.sc1",
                "EBS:SnapshotStorage-GB",
            ],
        },
        "EFS": {
            "base_rate": 0.3,
            "operations": ["FileOperations", "AccessOperations"],
            "price_range": (0.2, 0.8),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": ["EFS:Storage-GB", "EFS:InfrequentAccess-Storage-GB"],
        },
        "Glacier": {
            "base_rate": 0.004,
            "operations": [
                "ArchiveOperations",
                "RetrievalOperations",
                "DeepArchiveOperations",
            ],
            "price_range": (0.001, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": [
                "Storage-GB",
                "Retrieval-GB",
                "Archive",
                "Glacier:DeepArchive-Storage-GB",
            ],
        },
        "S3": {
            "base_rate": 0.023,
            "operations": ["StorageOperations", "DataTransfer", "TieringOperations"],
            "price_range": (0.001, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": [
                "Storage-GB",
                "DataTransfer-Out",
                "DataTransfer-In",
                "Requests-GET",
                "Requests-PUT",
                "Intelligent-Tiering-GB",
            ],
        },
        "Backup": {
            "base_rate": 0.05,
            "operations": ["BackupStorage", "BackupOperations", "RestoreOperations"],
            "price_range": (0.02, 0.1),
            "pricing_model": "on_demand",
            "unit": "GB-Month",
            "usage_types": ["BackupStorage-WarmStorage-GB-Month", "BackupStorage-ColdStorage-GB-Month"],
        },
    },
}

# Additional AWS Services that are defined in the projects but not in AWS_SERVICES
# Update AWS_SERVICES with additional services

# IoT category
AWS_SERVICES["IoT"] = {
    "IoT": {
        "base_rate": 0.08,
        "operations": ["MessageBroker", "DeviceRegistry", "RulesEngine"],
        "price_range": (0.05, 0.15),
        "pricing_model": "on_demand",
        "unit": "Million Messages",
        "usage_types": ["IoT-Messages", "IoT-Rules", "IoT-DeviceRegistry"],
    },
    "IoTSiteWise": {
        "base_rate": 0.10,
        "operations": ["DataCollection", "DataProcessing", "DataStorage"],
        "price_range": (0.05, 0.20),
        "pricing_model": "on_demand",
        "unit": "DataPoints",
        "usage_types": ["IoTSiteWise-DataPoints", "IoTSiteWise-Storage-GB-Month"],
    },
    "IoTAnalytics": {
        "base_rate": 0.25,
        "operations": ["DataIngestion", "DataStorage", "DataProcessing"],
        "price_range": (0.10, 0.50),
        "pricing_model": "on_demand",
        "unit": "GB",
        "usage_types": ["IoTAnalytics-Messages", "IoTAnalytics-Storage-GB-Month"],
    }
}

# Analytics extensions
AWS_SERVICES["Analytics"]["Kinesis"] = {
    "base_rate": 0.015,
    "operations": ["PutRecord", "GetRecord", "ShardHour"],
    "price_range": (0.01, 0.03),
    "pricing_model": "on_demand",
    "unit": "Shard-Hours",
    "usage_types": ["Kinesis-ShardHour", "Kinesis-PutRecords"],
}

AWS_SERVICES["Analytics"]["KinesisVideoStreams"] = {
    "base_rate": 0.0001,
    "operations": ["PutMedia", "GetMedia", "Storage"],
    "price_range": (0.00005, 0.0002),
    "pricing_model": "on_demand",
    "unit": "GB",
    "usage_types": ["KVS-DataIngestion-GB", "KVS-Storage-GB-Month", "KVS-GetHours"],
}

AWS_SERVICES["Analytics"]["ElasticSearch"] = {
    "base_rate": 0.10,
    "instance_types": ["t3.small.elasticsearch", "m5.large.elasticsearch", "c5.large.elasticsearch", "r5.large.elasticsearch"],
    "operations": ["SearchOperations", "IndexOperations", "StorageOperations"],
    "price_range": (0.05, 2.0),
    "pricing_model": "on_demand",
    "unit": "Hrs",
    "usage_types": ["ES-InstanceHours", "ES-Storage-GB"],
}

# Media Services
AWS_SERVICES["Media"] = {
    "MediaConvert": {
        "base_rate": 0.0075,
        "operations": ["VideoConversion", "AudioConversion", "Packaging"],
        "price_range": (0.005, 0.015),
        "pricing_model": "on_demand",
        "unit": "Minutes",
        "usage_types": ["MediaConvert-SD", "MediaConvert-HD", "MediaConvert-UHD"],
    },
    "MediaPackage": {
        "base_rate": 0.04,
        "operations": ["Ingest", "Origination", "Storage"],
        "price_range": (0.02, 0.08),
        "pricing_model": "on_demand",
        "unit": "GB",
        "usage_types": ["MediaPackage-Ingest-GB", "MediaPackage-Egress-GB"],
    },
    "MediaLive": {
        "base_rate": 0.2813,
        "operations": ["ChannelHours", "InputProcessing", "OutputProcessing"],
        "price_range": (0.15, 5.0),
        "pricing_model": "on_demand",
        "unit": "Hours",
        "usage_types": ["MediaLive-ChannelHours-SD", "MediaLive-ChannelHours-HD", "MediaLive-ChannelHours-UHD"],
    },
    "MediaConnect": {
        "base_rate": 0.08,
        "operations": ["FlowHours", "OutputHours", "DataTransfer"],
        "price_range": (0.05, 0.15),
        "pricing_model": "on_demand",
        "unit": "Hours",
        "usage_types": ["MediaConnect-FlowHours", "MediaConnect-OutputHours", "MediaConnect-DataTransfer-GB"],
    },
    "Elemental": {
        "base_rate": 0.15,
        "operations": ["EncodingHours", "TranscodingHours", "OutputHours"],
        "price_range": (0.10, 0.30),
        "pricing_model": "on_demand",
        "unit": "Hours",
        "usage_types": ["Elemental-EncodingHours", "Elemental-OutputHours"],
    },
}

# Security extensions
AWS_SERVICES["Security"]["Macie"] = {
    "base_rate": 1.0,
    "operations": ["DataClassification", "SensitiveDataDiscovery"],
    "price_range": (0.5, 2.0),
    "pricing_model": "on_demand",
    "unit": "GB",
    "usage_types": ["Macie-DataProcessed-GB", "Macie-SensitiveFindings"],
}

AWS_SERVICES["Security"]["CloudHSM"] = {
    "base_rate": 1.45,
    "operations": ["HSMInstance", "KeyOperations", "BackupOperations"],
    "price_range": (1.20, 2.0),
    "pricing_model": "hourly",
    "unit": "Hours",
    "usage_types": ["CloudHSM-InstanceHours", "CloudHSM-BackupStorage-GB"],
}

AWS_SERVICES["Security"]["Certificate Manager"] = {
    "base_rate": 0.75,
    "operations": ["CertificateIssuance", "CertificateRenewal"],
    "price_range": (0.0, 0.75),
    "pricing_model": "monthly",
    "unit": "Certificates-Month",
    "usage_types": ["ACM-PrivateCertificateAuthority-Month"],
}

# Healthcare Services
AWS_SERVICES["Healthcare"] = {
    "HealthLake": {
        "base_rate": 0.01,
        "operations": ["DataStorage", "DataImport", "DataQuery"],
        "price_range": (0.005, 0.02),
        "pricing_model": "on_demand",
        "unit": "GB-Month",
        "usage_types": ["HealthLake-Storage-GB-Month", "HealthLake-DataProcessing-GB"],
    },
}

# Compute extensions
AWS_SERVICES["Compute"]["EKS"] = {
    "base_rate": 0.10,
    "operations": ["ClusterOperations", "NodeOperations", "APIOperations"],
    "price_range": (0.10, 0.10),
    "pricing_model": "hourly",
    "unit": "Clusters-Hours",
    "usage_types": ["EKS-ClusterHours", "EKS-FargateUsage"],
}

AWS_SERVICES["Compute"]["Batch"] = {
    "base_rate": 0.0,  # Free service (pay only for underlying resources)
    "operations": ["SubmitJob", "ManageJob", "ScheduleJob"],
    "price_range": (0.0, 0.0),
    "pricing_model": "free",
    "unit": "Jobs",
    "usage_types": ["Batch-JobSubmissions", "Batch-JobScheduling"],
}

# Location Services
AWS_SERVICES["Location"] = {
    "Location": {
        "base_rate": 0.04,
        "operations": ["Maps", "Places", "Routes", "Tracking", "Geofencing"],
        "price_range": (0.02, 0.08),
        "pricing_model": "on_demand",
        "unit": "Requests",
        "usage_types": ["Location-MapTiles", "Location-Geocoding", "Location-Routes", "Location-Tracking"],
    },
}

# Networking extensions
AWS_SERVICES["Networking"]["AppMesh"] = {
    "base_rate": 0.012,
    "operations": ["MeshEndpoints", "VirtualNodes", "VirtualServices"],
    "price_range": (0.01, 0.02),
    "pricing_model": "hourly",
    "unit": "Resources-Hours",
    "usage_types": ["AppMesh-ResourceHours", "AppMesh-DataProcessed-GB"],
}

# Machine Learning extensions
AWS_SERVICES["Machine Learning"]["Translate"] = {
    "base_rate": 15.0,
    "operations": ["TextTranslation", "CustomTerminologyMapping"],
    "price_range": (10.0, 20.0),
    "pricing_model": "on_demand",
    "unit": "Million Characters",
    "usage_types": ["Translate-Characters", "Translate-CustomTerminology"],
}

# Fix naming variants
AWS_SERVICES["Application Integration"]["ApiGateway"] = AWS_SERVICES["Application Integration"]["APIGateway"]

#
#

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


ACCOUNT_HIERARCHY = {
    "Organization": {
        "account_id": "111111111111",  # Management Account
        "children": {
            "Core": {  # Core Organizational Unit
                "children": {
                    # Security Account
                    "Security": {"account_id": "555555555555"},
                    "SharedServices": {
                        "account_id": "666666666666"
                    },  # Shared Services Account
                    "Compliance": {
                        "account_id": "777777777777"
                    },  # Compliance/Audit Account
                }
            },
            "BusinessUnits": {  # Business Units OU
                "children": {
                    "Aviation": {  # Aviation BU
                        "children": {
                            "Aviation-Dev": {
                                "account_id": "222200000001"
                            },  # Aviation Dev
                            "Aviation-Staging": {
                                "account_id": "333300000001"
                            },  # Aviation Staging
                            "Aviation-Prod": {
                                "account_id": "444400000001"
                            },  # Aviation Prod
                            "Aviation-Analytics": {
                                "account_id": "888800000001"
                            },  # Aviation Analytics
                            "Aviation-IoT": {
                                "account_id": "999900000001"
                            },  # Aviation IoT - Added Missing Account
                        }
                    },
                    "Pharma": {  # Pharma BU
                        "children": {
                            # Pharma Dev
                            "Pharma-Dev": {"account_id": "222200000002"},
                            "Pharma-Staging": {
                                "account_id": "333300000002"
                            },  # Pharma Staging
                            "Pharma-Prod": {
                                "account_id": "444400000002"
                            },  # Pharma Prod
                            "Pharma-Research": {
                                "account_id": "888800000002"
                            },  # Pharma Research
                            "Pharma-Logistics": {
                                "account_id": "999900000002"
                            },  # Pharma Logistics - Added Missing Account
                        }
                    },
                    "Manufacturing": {  # Manufacturing BU
                        "children": {
                            "Manufacturing-Dev": {
                                "account_id": "222200000003"
                            },  # Manufacturing Dev
                            "Manufacturing-Staging": {
                                "account_id": "333300000003"
                            },  # Manufacturing Staging
                            "Manufacturing-Prod": {
                                "account_id": "444400000003"
                            },  # Manufacturing Prod
                            "Manufacturing-IoT": {
                                "account_id": "888800000003"
                            },  # Manufacturing IoT
                            "Manufacturing-Logistics": {
                                "account_id": "999900000003"
                            },  # Manufacturing Logistics - Added Missing Account
                        }
                    },
                    "SupplyChain": {  # Supply Chain BU
                        "children": {
                            "SupplyChain-Dev": {
                                "account_id": "222200000004"
                            },  # Supply Chain Dev
                            "SupplyChain-Staging": {
                                "account_id": "333300000004"
                            },  # Supply Chain Staging
                            "SupplyChain-Prod": {
                                "account_id": "444400000004"
                            },  # Supply Chain Prod
                            "SupplyChain-Logistics": {
                                "account_id": "888800000004"
                            },  # Supply Chain Logistics
                            "SupplyChain-Analytics": {
                                "account_id": "999900000004"
                            },  # Supply Chain Analytics - Added Missing Account
                        }
                    },
                    "SoftwareSolutions": {  # Software Solutions BU - SaaS Business
                        "children": {
                            "SoftwareSolutions-Dev": {
                                "account_id": "222200000005"
                            },  # Software Solutions Dev
                            "SoftwareSolutions-Staging": {
                                "account_id": "333300000005"
                            },  # Software Solutions Staging
                            "SoftwareSolutions-Prod": {
                                "account_id": "444400000005"
                            },  # Software Solutions Prod
                            "SoftwareSolutions-CustomerData": {
                                "account_id": "888800000005"
                            },  # Software Solutions Customer Data - Isolated for sensitive data
                            "SoftwareSolutions-Analytics": {
                                "account_id": "999900000005"
                            },  # Software Solutions Analytics - Added Missing Account
                        }
                    },
                    "MachineLearning": {  # Machine Learning Center of Excellence
                        "children": {
                            # ML Dev/Sandbox
                            "ML-Dev": {"account_id": "222200000006"},
                            "ML-Staging": {
                                "account_id": "333300000006"
                            },  # ML Staging/Pre-Prod
                            "ML-Prod": {
                                "account_id": "444400000006"
                            },  # ML Prod/Inference
                            "ML-FeatureStore": {
                                "account_id": "888800000006"
                            },  # ML Feature Store Account - Centralized Data
                            "ML-Analytics": {
                                "account_id": "999900000006"
                            },  # ML Analytics - Added Missing Account
                        }
                    },
                }
            },
            "Sandbox": {  # Centralized Sandbox OU for ad-hoc experiments
                "children": {
                    "Sandbox-Central": {
                        "account_id": "222299999999"
                    }  # Central Sandbox Account
                }
            },
        },
    }
}


PROJECT_LIFECYCLES = [
    "growing",
    "growing_then_sunset",
    "just_started",
    "steady_state",
    "declining",
    "peak_and_plateau",
    "decomissioned"
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
]  # More stages to align with hierarchy

CONFIGURABLES = {
    # "number_of_days": 11111,
    "number_of_days": 365,
    "annual_budget": 250000000,  # Increased Annual Budget for larger scale
    "usage_growth_rate": {
        "growing": 1.002,
        "growing_then_sunset": 1.001,
        "just_started": 1.0005,
        "steady_state": 1.00005,  # Reduced steady state growth
        "declining": 0.999,
        "peak_and_plateau": 1.0002,  # Slow growth to plateau
    },
    "sunset_start_day_ratio": 0.6,
    "sunset_decline_rate": 0.997,
    # Plateau starts at 40% of days for peak_and_plateau
    "peak_plateau_start_day_ratio": 0.4,
    "peak_plateau_duration_ratio": 0.4,  # Plateau lasts for 40% of days
}


CONFIG = {
    "number_of_days": CONFIGURABLES["number_of_days"],
    "annual_budget": CONFIGURABLES["annual_budget"],
    "services": AWS_SERVICES,
    "use_case_scenarios": USE_CASE_SCENARIOS,
    "account_hierarchy": ACCOUNT_HIERARCHY,
    "project_lifecycles": PROJECT_LIFECYCLES,
    "project_stages": PROJECT_STAGES,
    "configurables": CONFIGURABLES,
    "AWS_REGIONS": AWS_REGIONS,
    "REGIONAL_COST_FACTORS": REGIONAL_COST_FACTORS,
    "projects": {
        # Aviation Business Unit Projects (5 Projects)
        "AerodynamicPerformanceAnalysis": {
            "description": "Aircraft aerodynamic performance analysis using cloud-based ETL and analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "S3",
                "Glue",
                "Athena",
                "EMR",
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "QuickSight",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["aviation-analytics"],  # Aviation Analytics Account
            "business_unit": "Aviation",
        },
        "SkyConnectPassengerApp": {
            "description": "Mobile application for airline passengers providing flight information and services.",
            "use_case": "Mobile Applications",
            "lifecycle": "peak_and_plateau",  # Mature Mobile App
            "services": [
                "Lambda",
                "DynamoDB",
                "APIGateway",
                "Cognito",
                "CloudFront",
                "SNS",
                "CloudWatchLogs",
                "WAF",
            ],  # Corrected Service Name
            # Aviation Prod and Dev
            "stages": ["aviation-prod", "aviation-dev"],
            "business_unit": "Aviation",
        },
        "GuardianAirTrafficControl": {
            "description": "Mission-critical air traffic control system ensuring safe and efficient flight operations.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",  # Critical System
            "services": [
                "EC2",
                "RDS",
                "AutoScaling",
                "VPC",
                "DirectConnect",
                "CloudWatchLogs",
                "CloudTrail",
                "Route53",
            ],  # Corrected Service Name
            "stages": [
                "aviation-prod",
                "aviation-staging",
            ],  # Aviation Prod and Staging
            "business_unit": "Aviation",
        },
        "RunwayOperationsMonitoring": {
            "description": "Real-time monitoring and analytics of runway conditions and airport operations.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "growing",
            "services": [
                "CloudWatch",
                "ManagedGrafana",
                "CloudWatchSynthetics",
                "CloudWatchLogs",
                "CloudTrail",
            ],
            "stages": ["aviation-analytics"],  # Aviation Analytics Account
            "business_unit": "Aviation",
        },
        "JetEngineTelemetryAnalysis": {
            "description": "Advanced analytics of jet engine telemetry data for performance optimization and predictive maintenance.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "S3",
                "Glue",
                "Athena",
                "Redshift",
                "QuickSight",
                "EMR",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "aviation-iot",
                "aviation-analytics",
            ],  # Hypothetical Aviation IoT and Analytics accounts (not explicitly in hierarchy, but could be added)
            "business_unit": "Aviation",
        },
        # Pharma Business Unit Projects (8 Projects)
        "MoleculeSynthesizerAI": {
            "description": "AI-driven platform for synthesizing novel molecules for pharmaceutical research and development.",
            "use_case": "Generative AI and LLMs",  # Use GenAI use case
            "lifecycle": "growing",
            "services": [
                "SageMaker",
                "SageMakerFeatureStore",
                "SageMakerInference",
                "SageMakerGroundTruth",
                "EC2",
                "S3",
                "Glue",
                "DynamoDB",
                "Bedrock",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "pharma-research",
                "pharma-staging",
                "pharma-prod",
            ],  # Pharma Research, Staging, Prod
            "business_unit": "Pharma",
        },
        "TrialMasterClinicalPlatform": {
            "description": "Comprehensive platform for managing and executing clinical trials, ensuring compliance and data integrity.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2",
                "RDS",
                "APIGateway",
                "Cognito",
                "CloudWatchLogs",
                "CloudTrail",
                "WAF",
                "SNS",
            ],  # Corrected Service Name
            # Pharma Prod and Staging
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "PillProductionQualityControl": {
            "description": "Machine learning system for real-time quality control in pharmaceutical pill production.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "S3",
                "Glue",
                "QuickSight",
                "EMR",
                "Timestream",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            # Pharma Prod and Staging
            "stages": ["pharma-prod", "pharma-staging"],
            "business_unit": "Pharma",
        },
        "GenomeAnalyticsWorkbench": {
            "description": "Advanced workbench for genomic data analysis, enabling faster and more accurate research.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "S3",
                "Glue",
                "Athena",
                "EMR",
                "Redshift",
                "LakeFormation",
                "EC2",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "pharma-research",
                "pharma-analytics",
            ],  # Pharma Research, Analytics
            "business_unit": "Pharma",
        },
        "PersonalizedDrugRecommendationEngine": {
            "description": "Generative AI engine to provide personalized drug recommendations based on patient profiles.",
            "use_case": "Generative AI and LLMs",  # Use GenAI use case
            "lifecycle": "just_started",
            "services": [
                "SageMaker",
                "SageMakerInference",
                "SageMakerFeatureStore",
                "Bedrock",
                "Comprehend",
                "Lex",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["pharma-research"],  # Pharma Research Account
            "business_unit": "Pharma",
        },
        "GxPComplianceDashboard": {
            "description": "Dashboard to monitor and ensure GxP compliance across pharmaceutical production and research.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "Config",
                "AuditManager",
                "SecurityHub",
                "CloudWatchLogs",
                "CloudTrail",
            ],  # Compliance focused services
            "stages": [
                "pharma-prod",
                "compliance",
            ],  # Pharma Prod and Central Compliance
            "business_unit": "Pharma",
        },
        "MediSupplyChainTracker": {
            "description": "Real-time tracking and visibility platform for the medical supply chain, improving logistics and efficiency.",
            "use_case": "Enterprise Integration",  # More generic integration use case
            "lifecycle": "growing",
            "services": [
                "EventBridge",
                "SQS",
                "SNS",
                "DynamoDB",
                "APIGateway",
                "QuickSight",
                "Lambda",
                "MSK",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            # Hypothetical Pharma Logistics account
            "stages": ["pharma-logistics"],
            "business_unit": "Pharma",
        },
        "RDExperimentDataPipeline": {
            "description": "Automated data pipeline for managing and processing research and development experiment data.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "Glue",
                "StepFunctions",
                "S3",
                "EC2",
                "SageMaker",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["pharma-research"],  # Pharma Research
            "business_unit": "Pharma",
        },
        # Manufacturing Business Unit Projects (7 Projects)
        "SmartFactoryRealTimeData": {
            "description": "Real-time data platform for smart factory operations, collecting and analyzing sensor data from manufacturing equipment.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "S3",
                "Glue",
                "Timestream",
                "QuickSight",
                "EMR",
                "MSK",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "manufacturing-iot",
                "manufacturing-analytics",
                "manufacturing-prod",
            ],  # Manufacturing IoT, Analytics, Prod
            "business_unit": "Manufacturing",
        },
        "EquipmentPredictiveMaintenance": {
            "description": "Predictive maintenance system using machine learning to forecast equipment failures and optimize maintenance schedules.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "SageMaker",
                "SageMakerInference",
                "SageMakerFeatureStore",
                "S3",
                "DynamoDB",
                "KinesisDataFirehose",
                "QuickSight",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "manufacturing-prod",
                "manufacturing-staging",
                "manufacturing-analytics",
            ],  # Manufacturing Prod, Staging, Analytics
            "business_unit": "Manufacturing",
        },
        "ComponentSupplyChainVisibility": {
            "description": "Platform for enhanced visibility and tracking of components across the manufacturing supply chain.",
            "use_case": "Enterprise Integration",  # More generic integration use case
            "lifecycle": "growing",
            "services": [
                "EventBridge",
                "SQS",
                "SNS",
                "DynamoDB",
                "APIGateway",
                "QuickSight",
                "Lambda",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "manufacturing-logistics",
                "manufacturing-prod",
            ],  # Hypothetical Manufacturing Logistics
            "business_unit": "Manufacturing",
        },
        "AutomatedQualityInspection": {
            "description": "Automated visual quality inspection system for manufactured products using AI and computer vision.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "Rekognition",
                "S3",
                "Lambda",
                "APIGateway",
                "StepFunctions",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "manufacturing-prod",
                "manufacturing-staging",
            ],  # Manufacturing Prod and Staging
            "business_unit": "Manufacturing",
        },
        "ProductionLineDashboard": {
            "description": "Real-time dashboard providing key performance indicators and operational insights for manufacturing production lines.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudWatch",
                "CloudWatchLogs",
                "CloudWatchSynthetics",
                "XRay",
                "KinesisDataFirehose",
            ],
            "stages": [
                "manufacturing-prod",
                "manufacturing-iot",
            ],  # Manufacturing Prod and IoT
            "business_unit": "Manufacturing",
        },
        "EnterpriseResourcePlanning": {
            "description": "Comprehensive ERP system to manage all aspects of manufacturing operations, from resource planning to financial management.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",  # Mature ERP system
            "services": [
                "EC2",
                "RDS",
                "AutoScaling",
                "VPC",
                "DirectConnect",
                "CloudWatchLogs",
                "CloudTrail",
                "Route53",
            ],  # Corrected Service Name
            "stages": [
                "manufacturing-prod",
                "manufacturing-staging",
            ],  # Manufacturing Prod and Staging
            "business_unit": "Manufacturing",
        },
        "FactoryFloorComplianceSystem": {
            "description": "System to ensure factory floor operations adhere to industry regulations and compliance standards.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "Config",
                "AuditManager",
                "SecurityHub",
                "CloudWatchLogs",
                "CloudTrail",
            ],  # Compliance services
            "stages": [
                "manufacturing-prod",
                "compliance",
            ],  # Manufacturing Prod and Central Compliance
            "business_unit": "Manufacturing",
        },
        # Supply Chain Business Unit Projects (7 Projects)
        "GlobalShipmentTracker": {
            "description": "Global shipment tracking platform providing end-to-end visibility for all shipments across the supply chain.",
            "use_case": "Enterprise Integration",  # More generic integration use case
            "lifecycle": "growing",
            "services": [
                "EventBridge",
                "SQS",
                "SNS",
                "DynamoDB",
                "APIGateway",
                "QuickSight",
                "Lambda",
                "MSK",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-logistics",
                "supplychain-prod",
                "supplychain-staging",
            ],  # Supply Chain Logistics, Prod, Staging
            "business_unit": "SupplyChain",
        },
        "WarehouseManagementApp": {
            "description": "Application for managing warehouse operations, inventory, and order fulfillment.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2",
                "RDS",
                "AutoScaling",
                "VPC",
                "CloudFront",
                "WAF",
                "CloudWatchLogs",
                "Route53",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-prod",
                "supplychain-staging",
            ],  # Supply Chain Prod and Staging
            "business_unit": "SupplyChain",
        },
        "SupplierSelfServicePortal": {
            "description": "Self-service portal for suppliers to manage orders, invoices, and communication with the organization.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",  # Mature supplier portal
            "services": [
                "EC2",
                "RDS",
                "APIGateway",
                "Cognito",
                "CloudFront",
                "WAF",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-prod",
                "supplychain-staging",
            ],  # Supply Chain Prod and Staging
            "business_unit": "SupplyChain",
        },
        "DemandForecastAI": {
            "description": "AI-powered demand forecasting system to predict future demand and optimize inventory levels.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "SageMaker",
                "SageMakerInference",
                "SageMakerFeatureStore",
                "S3",
                "Glue",
                "Athena",
                "QuickSight",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-analytics",
                "supplychain-staging",
                "supplychain-prod",
            ],  # Supply Chain Analytics, Staging, Prod
            "business_unit": "SupplyChain",
        },
        "RouteOptimizationEngine": {
            "description": "Engine for optimizing delivery routes and logistics operations to reduce costs and improve delivery times.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "Glue",
                "Athena",
                "EMR",
                "Redshift",
                "S3",
                "StepFunctions",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-logistics",
                "supplychain-analytics",
            ],  # Supply Chain Logistics and Analytics
            "business_unit": "SupplyChain",
        },
        "InventoryVisibilityPlatform": {
            "description": "Platform providing real-time visibility into inventory levels and locations across the entire supply chain network.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "Timestream",
                "S3",
                "QuickSight",
                "Lambda",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "supplychain-logistics",
                "supplychain-prod",
            ],  # Supply Chain Logistics and Prod
            "business_unit": "SupplyChain",
        },
        "TradeComplianceMonitor": {
            "description": "System to monitor and ensure compliance with international trade regulations and tariffs.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "Config",
                "AuditManager",
                "SecurityHub",
                "CloudWatchLogs",
                "CloudTrail",
            ],  # Compliance services
            "stages": [
                "supplychain-prod",
                "compliance",
            ],  # Supply Chain Prod and Central Compliance
            "business_unit": "SupplyChain",
        },
        # Software Solutions Business Unit Projects (8 Projects)
        "CloudAppSaaSBackend": {
            "description": "Backend infrastructure for a SaaS application providing core services and data management.",
            "use_case": "Software Solutions",
            "lifecycle": "growing",
            "services": [
                "EC2",
                "ECS",
                "RDS",
                "DynamoDB",
                "AutoScaling",
                "APIGateway",
                "Lambda",
                "ElastiCache",
                "MSK",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "softwaresolutions-prod",
                "softwaresolutions-staging",
            ],  # Software Solutions Prod and Staging
            "business_unit": "SoftwareSolutions",
        },
        "CustomerServiceHelpCenter": {
            "description": "Online help center and support portal for SaaS customers, offering knowledge base and ticketing system.",
            "use_case": "Software Solutions",
            "lifecycle": "peak_and_plateau",  # Mature customer portal
            "services": [
                "EC2",
                "RDS",
                "APIGateway",
                "Cognito",
                "CloudFront",
                "WAF",
                "CloudWatchLogs",
                "Route53",
            ],  # Corrected Service Name
            "stages": [
                "softwaresolutions-prod",
                "softwaresolutions-staging",
            ],  # Software Solutions Prod and Staging
            "business_unit": "SoftwareSolutions",
        },
        "TeamCollaborationHub": {
            "description": "Enterprise-grade team collaboration and communication platform for internal company use.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2",
                "RDS",
                "AutoScaling",
                "VPC",
                "DirectConnect",
                "CloudWatchLogs",
                "CloudTrail",
                "Route53",
            ],  # Corrected Service Name
            "stages": [
                "softwaresolutions-prod",
                "softwaresolutions-staging",
            ],  # Software Solutions Prod and Staging
            "business_unit": "SoftwareSolutions",
        },
        "SaaSCustomerInsights": {
            "description": "Analytics and business intelligence platform providing insights into SaaS customer usage and behavior.",
            "use_case": "Analytics",
            "lifecycle": "growing",
            "services": [
                "Athena",
                "QuickSight",
                "Glue",
                "S3",
                "Redshift",
                "EMR",
                "KinesisDataFirehose",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "softwaresolutions-customerdata",
                "softwaresolutions-analytics",
                "softwaresolutions-prod",
            ],  # Software Solutions Customer Data, Analytics, Prod - Customer Data isolated
            "business_unit": "SoftwareSolutions",
        },
        "FeatureRolloutManager": {
            "description": "System to manage and control the rollout of new features to SaaS customers, enabling gradual releases and A/B testing.",
            "use_case": "Software Solutions",
            "lifecycle": "just_started",
            "services": [
                "Lambda",
                "DynamoDB",
                "APIGateway",
                "StepFunctions",
                "EventBridge",
                "SNS",
                "SQS",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["softwaresolutions-dev"],  # Software Solutions Dev
            "business_unit": "SoftwareSolutions",
        },
        "CustomerDataLakehouse": {
            "description": "Scalable data lakehouse for storing and analyzing customer data to improve SaaS offering and customer experience.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "S3",
                "Glue",
                "LakeFormation",
                "Athena",
                "EMR",
                "Redshift",
                "SecurityLake",
                "GuardDuty",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": [
                "softwaresolutions-customerdata"
            ],  # Software Solutions Customer Data
            "business_unit": "SoftwareSolutions",
        },
        "CloudServiceTrustPlatform": {
            "description": "Platform to demonstrate and manage trust and compliance for the SaaS offering, addressing security and regulatory requirements.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "Config",
                "AuditManager",
                "SecurityHub",
                "CloudWatchLogs",
                "CloudTrail",
            ],  # Compliance services
            "stages": [
                "softwaresolutions-prod",
                "compliance",
            ],  # Software Solutions Prod and Central Compliance
            "business_unit": "SoftwareSolutions",
        },
        "AIHelpdeskChatbot": {
            "description": "AI-powered chatbot to provide automated customer support and answer common helpdesk queries.",
            "use_case": "Generative AI and LLMs",  # Use GenAI use case
            "lifecycle": "just_started",
            "services": [
                "Bedrock",
                "Lex",
                "Comprehend",
                "SageMakerInference",
                "Lambda",
                "DynamoDB",
                "APIGateway",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["softwaresolutions-dev"],  # Software Solutions Dev
            "business_unit": "SoftwareSolutions",
        },
        # Machine Learning Center of Excellence Projects (7 Projects)
        "CentralizedFeatureRepository": {
            "description": "Centralized repository to store, manage, and share features for machine learning models across the organization.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "SageMakerFeatureStore",
                "S3",
                "Glue",
                "LakeFormation",
                "Athena",
                "Redshift",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-featurestore"],  # ML Feature Store account
            "business_unit": "MachineLearning",
        },
        "ModelDeploymentPipeline": {
            "description": "Automated pipeline for deploying and managing machine learning models to production environments.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "SageMaker",
                "SageMakerFeatureStore",
                "S3",
                "DynamoDB",
                "StepFunctions",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-staging", "ml-prod"],  # ML Staging and Prod
            "business_unit": "MachineLearning",
        },
        "SharedTrainingCompute": {
            "description": "Shared, scalable compute infrastructure for machine learning training workloads across different teams.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "SageMaker",
                "EC2",
                "EBS",
                "S3",
                "SystemsManager",
                "AutoScaling",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-staging"],  # ML Staging
            "business_unit": "MachineLearning",
        },
        "RealTimeAnomalyDetection": {
            "description": "Real-time anomaly detection system to identify and alert on anomalies in data streams and system behavior.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "growing",
            "services": [
                "SageMaker",
                "SageMakerInference",
                "S3",
                "KinesisDataStreams",
                "KinesisDataFirehose",
                "QuickSight",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-prod", "ml-staging"],  # ML Prod and Staging
            "business_unit": "MachineLearning",
        },
        "GenAIModelHub": {
            "description": "Centralized hub for managing, deploying, and accessing generative AI models across the organization.",
            "use_case": "Generative AI and LLMs",  # Use GenAI use case
            "lifecycle": "growing",
            "services": [
                "SageMakerInference",
                "EC2",
                "ECS",
                "APIGateway",
                "CloudFront",
                "WAF",
                "AutoScaling",
                "Bedrock",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-prod"],  # ML Prod
            "business_unit": "MachineLearning",
        },
        "MLOpsAutomationFramework": {
            "description": "Framework and tools for automating machine learning operations (MLOps), including model training, deployment, and monitoring.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "steady_state",
            "services": [
                "StepFunctions",
                "EventBridge",
                "CodePipeline",
                "CodeBuild",
                "CodeDeploy",
                "SNS",
                "SQS",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["ml-staging", "ml-prod"],  # ML Staging and Prod
            "business_unit": "MachineLearning",
        },
        "MLSandboxEnvironment": {
            "description": "Isolated sandbox environment for data scientists and ML engineers to experiment, prototype, and develop ML solutions.",
            "use_case": "Machine Learning and AI",  # Corrected to general ML use case
            "lifecycle": "just_started",
            "services": [
                "SageMaker",
                "EC2",
                "S3",
                "DynamoDB",
                "QuickSight",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["sandbox-central"],  # Central Sandbox Account
            "business_unit": "MachineLearning",
        },
        # Core/Shared Services/Security/Compliance Projects (15 Projects)
        "ThreatDetectionCenter": {
            "description": "Centralized threat detection and incident response center for proactive security monitoring and alerting.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "SecurityHub",
                "GuardDuty",
                "SecurityLake",
                "CloudWatchLogs",
                "CloudTrail",
                "IAMAccessAnalyzer",
                "Config",
            ],  # Centralized security monitoring
            "stages": ["security"],  # Security Account
            "business_unit": "Core",
        },
        "EnterpriseLoggingService": {
            "description": "Centralized logging service for collecting, storing, and analyzing logs from across the entire AWS environment.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudWatchLogs",
                "KinesisDataFirehose",
                "S3",
                "Glacier",
                "CloudTrail",
                "VPC",
            ],  # Replaced "VPC Flow Logs" with VPC, as VPC itself can incur cost
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "IdentityLifecycleManagement": {
            "description": "Service for managing the lifecycle of user identities and access across the organization's AWS footprint.",
            "use_case": "Security",  # Use Case refined to "Security"
            "lifecycle": "steady_state",
            "services": [
                "IAM",
                "IAMIdentityCenter",
                "KMS",
                "SecretsManager",
                "Config",
            ],  # Centralized Identity Management
            "stages": ["security"],  # Security Account
            "business_unit": "Core",
        },
        "CorporateNetworkProtection": {
            "description": "Comprehensive network security infrastructure to protect the organization's cloud and on-premises networks.",
            "use_case": "Security",  # Use Case refined to "Security"
            "lifecycle": "steady_state",
            "services": [
                "VPC",
                "NetworkFirewall",
                "WAF",
                "ShieldAdvanced",
                "Route53",
                "DirectConnect",
            ],  # Network Security Infrastructure
            "stages": ["security"],  # Security Account
            "business_unit": "Core",
        },
        "CloudCostOptimizationProgram": {
            "description": "Program dedicated to continuously monitor and optimize cloud spending, ensuring cost efficiency across all AWS accounts.",
            "use_case": "Management & Governance",  # Management & Governance Use Case
            "lifecycle": "steady_state",
            "services": [
                "CostExplorer",
                "CloudWatchLogs",
            ],  # Corrected Service Name and Removed non-cost incurring services
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "CentralizedBackupService": {
            "description": "Centralized service providing backup and recovery for critical data and systems across the organization's AWS environment.",
            "use_case": "Storage",  # Storage Use Case for Backup
            "lifecycle": "steady_state",
            "services": [
                "Backup",
                "S3",
                "EBS",
                "RDS",
                "Glacier",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "AutomatedPatchManagement": {
            "description": "Automated system for patching operating systems and applications across the organization's EC2 instances and servers.",
            "use_case": "Management & Governance",  # Management & Governance Use Case
            "lifecycle": "steady_state",
            "services": [
                "SystemsManager",
                "Config",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "InfrastructureVulnerabilityScanner": {
            "description": "Automated vulnerability scanning service to identify and report security vulnerabilities in the organization's cloud infrastructure.",
            "use_case": "Security",  # Use Case refined to "Security"
            "lifecycle": "steady_state",
            "services": [
                "Inspector",
                "SecurityHub",
                "SystemsManager",
                "EC2",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["security"],  # Security Account
            "business_unit": "Core",
        },
        "ComplianceReportingEngine": {
            "description": "Engine to automate the generation of compliance reports and dashboards for various regulatory frameworks.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "AuditManager",
                "Config",
                "SecurityHub",
                "CloudWatchLogs",
                "CloudTrail",
                "Athena",
                "QuickSight",
            ],  # Compliance Reporting Framework
            "stages": ["compliance"],  # Compliance Account
            "business_unit": "Core",
        },
        "DisasterRecoveryDrills": {
            "description": "Orchestration and execution of disaster recovery drills to test and improve the organization's DR capabilities.",
            # Changed use case to compliance as DR testing is often for compliance
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "EC2",
                "RDS",
                "Route53",
                "CloudWatchLogs",
                "CloudTrail",
                "EC2",
            ],  # Corrected Service Name and Replaced "Site Recovery" with EC2, as Site Recovery replicates EC2 instances. Added EC2 again for cost.
            "stages": [
                "shared-services"
            ],  # Shared Services Account - Corrected stage alias
            "business_unit": "Core",
        },
        "CentralizedMonitoringDashboards": {
            "description": "Centralized monitoring dashboards providing a unified view of the health and performance of the organization's AWS environment.",
            "use_case": "Monitoring, Logging and Observability",
            "lifecycle": "steady_state",
            "services": [
                "CloudWatch",
                "ManagedGrafana",
                "QuickSight",
                "CloudWatchLogs",
                "CloudTrail",
            ],  # Centralized Dashboards
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "InfraPipelineOrchestrator": {
            "description": "Centralized infrastructure pipeline orchestrator for automating the deployment and management of AWS infrastructure.",
            "use_case": "Management & Governance",
            "lifecycle": "steady_state",
            "services": [
                "CodePipeline",
                "CodeBuild",
                "CodeDeploy",
                "CloudFormation",
                "SystemsManager",
                "CloudTrail",
                "CloudWatchLogs",
            ],  # Corrected Service Name
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "EnterpriseDNSPlatform": {
            "description": "Enterprise-grade DNS platform providing reliable and scalable DNS services for the organization.",
            "use_case": "Networking",
            "lifecycle": "steady_state",
            # Corrected Service Name
            "services": ["Route53", "CloudWatchLogs"],
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "CrossAccountBackupService": {
            "description": "Cross-account backup service enabling centralized backup and recovery management across multiple AWS accounts.",
            "use_case": "Storage",
            "lifecycle": "steady_state",
            "services": [
                "Backup",
                "S3",
                "Glacier",
                "CloudWatchLogs",
            ],  # Corrected Service Name and Removed "Data Lifecycle Manager", using core backup and storage services
            "stages": ["shared-services"],  # Shared Services Account
            "business_unit": "Core",
        },
        "SharedServicesDevSandbox": {
            "description": "Centralized sandbox environment for the Shared Services team to develop and test new infrastructure and automation.",
            "use_case": "Management & Governance",
            "lifecycle": "just_started",
            "services": [
                "EC2",
                "Lambda",
                "S3",
                "CloudWatchLogs",
            ],  # Corrected Service Name and Minimal Sandbox Services
            "stages": ["sandbox-central"],  # Central Sandbox Account
            "business_unit": "Core",
        },
        # Enterprise Data Platform Projects
        "GlobalDataLakehouse": {
            "description": "Enterprise-wide data lakehouse platform integrating structured and unstructured data across all business units, with centralized governance, ML-ready datasets, and self-service analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "S3", "Glue", "Athena", "LakeFormation", "EMR", "Redshift",
                "QuickSight", "Lambda", "StepFunctions", "CloudWatchLogs",
                "IAMIdentityCenter", "KMS", "CloudTrail"
            ],
            "stages": ["shared-services", "ml-featurestore"],
            "business_unit": "Core",
        },
        "MultiRegionStreamingDataPipeline": {
            "description": "Global, fault-tolerant streaming data pipeline with multi-region replication, handling 10+ TB daily across 5 continents with sub-second latency requirements.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "KinesisDataStreams", "KinesisDataFirehose", "MSK", "S3",
                "Lambda", "DynamoDB", "DynamoDB", "CloudFront", "Route53",
                "CloudWatchLogs", "EventBridge", "SQS", "CloudWatch"
            ],
            "stages": ["shared-services", "supplychain-analytics", "manufacturing-iot"],
            "business_unit": "SupplyChain",
        },
        "RegulatoryReportingDataWarehouse": {
            "description": "Centralized regulatory reporting platform integrating financial, risk, and compliance data with point-in-time recovery and full audit trails for financial regulations.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "steady_state",
            "services": [
                "Redshift", "S3", "Glue", "Athena", "QuickSight",
                "Lambda", "StepFunctions", "CloudWatchLogs", "CloudTrail",
                "Backup", "KMS", "Config", "AuditManager"
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
                "EC2", "ECS", "RDS", "DynamoDB", "ElastiCache", "Lambda",
                "APIGateway", "CloudFront", "Route53", "S3", "SQS", "SNS",
                "Cognito", "CloudWatchLogs", "XRay", "WAF"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "GlobalECommerceInfrastructure": {
            "description": "High-volume, global e-commerce platform handling millions of transactions daily with 99.99% availability across multiple regions and dynamic scaling during peak seasons.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2", "RDS", "DynamoDB", "ElastiCache", "CloudFront",
                "Route53", "S3", "ECS", "SNS", "SQS", "APIGateway",
                "Lambda", "CloudWatchLogs", "CloudWatch", "WAF",
                "ShieldAdvanced", "IAM", "KMS"
            ],
            "stages": ["supplychain-prod", "supplychain-staging"],
            "business_unit": "SupplyChain",
        },
        "MultiLanguageContentPlatform": {
            "description": "Enterprise content management platform supporting 40+ languages with distributed authoring, automated translation workflows, and global content delivery.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2", "RDS", "S3", "CloudFront", "Lambda", "SQS",
                "ElastiCache", "Comprehend", "CloudWatchLogs", "Translate",
                "StepFunctions", "IAM", "Cognito"
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
                "SageMaker", "SageMakerInference", "Bedrock", "S3",
                "Lambda", "EFS", "APIGateway", "CloudFront", "EC2",
                "SecretsManager", "CloudWatchLogs", "KMS"
            ],
            "stages": ["ml-prod", "ml-staging"],
            "business_unit": "MachineLearning",
        },
        "VideoAnalyticsSecuritySystem": {
            "description": "Enterprise video surveillance analytics system processing feeds from 10,000+ cameras with real-time object detection, anomaly detection, and secure retention.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "Rekognition", "Kinesis", "KinesisVideoStreams", "S3",
                "Lambda", "DynamoDB", "EC2", "ECS", "SageMakerInference",
                "CloudWatchLogs", "IAM", "KMS", "CloudWatch"
            ],
            "stages": ["security", "ml-prod"],
            "business_unit": "Security",
        },
        "PredictiveMaintenanceSystem": {
            "description": "Industrial-scale predictive maintenance system processing terabytes of sensor data daily from 50,000+ connected devices to forecast equipment failures.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "IoT", "IoTAnalytics", "KinesisDataStreams", "S3",
                "SageMaker", "Lambda", "DynamoDB", "SNS", "Timestream",
                "QuickSight", "CloudWatchLogs", "EMR"
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
                "IoT", "IoTSiteWise", "KinesisDataStreams", "Timestream",
                "S3", "Lambda", "DynamoDB", "SNS", "SageMaker",
                "CloudWatchLogs", "QuickSight", "EC2", "EKS"
            ],
            "stages": ["manufacturing-iot", "manufacturing-prod", "manufacturing-analytics"],
            "business_unit": "Manufacturing",
        },
        "ConnectedAircraftAnalytics": {
            "description": "Aviation telematics platform processing in-flight data from 500+ aircraft, with edge computing capabilities, satellite connectivity, and predictive analytics.",
            "use_case": "Data Processing and ETL",
            "lifecycle": "growing",
            "services": [
                "IoT", "IoTAnalytics", "S3", "KinesisDataStreams",
                "Glue", "Athena", "EMR", "Lambda", "SageMaker",
                "CloudWatchLogs", "QuickSight", "Redshift"
            ],
            "stages": ["aviation-iot", "aviation-analytics"],
            "business_unit": "Aviation",
        },
        "GlobalLogisticsTrackingNetwork": {
            "description": "Worldwide logistics tracking system monitoring millions of shipments in real-time across global supply chains with predictive ETAs and disruption management.",
            "use_case": "Enterprise Integration",
            "lifecycle": "steady_state",
            "services": [
                "IoT", "KinesisDataStreams", "S3", "DynamoDB", "Lambda",
                "ApiGateway", "CloudFront", "EC2", "EventBridge",
                "StepFunctions", "CloudWatchLogs", "EMR"
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
                "EC2", "RDS", "DynamoDB", "ElastiCache", "Lambda",
                "StepFunctions", "SQS", "KMS", "CloudHSM", "WAF",
                "CloudWatchLogs", "CloudTrail", "Config"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "EnterpriseFinancialReportingSystem": {
            "description": "Consolidated financial reporting platform integrating data from 50+ global subsidiaries with multi-currency support, complex allocations, and regulatory compliance.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "EC2", "RDS", "S3", "Lambda", "StepFunctions",
                "QuickSight", "Glue", "Athena", "CloudWatchLogs",
                "KMS", "Config", "CloudTrail"
            ],
            "stages": ["softwaresolutions-prod", "compliance"],
            "business_unit": "SoftwareSolutions",
        },
        "TaxCalculationEngine": {
            "description": "Global tax calculation engine with coverage for 120+ countries, handling millions of complex tax determinations daily with automatic regulatory updates.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "EC2", "RDS", "Lambda", "APIGateway", "S3",
                "DynamoDB", "CloudFront", "ECS", "CloudWatchLogs",
                "CloudTrail", "KMS", "Config"
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
                "SecurityHub", "GuardDuty", "Inspector", "Macie",
                "SecurityLake", "CloudTrail", "CloudWatchLogs", "Lambda",
                "EventBridge", "StepFunctions", "SNS", "KMS"
            ],
            "stages": ["security", "compliance"],
            "business_unit": "Core",
        },
        "DataPrivacyCompliancePlatform": {
            "description": "Enterprise platform for managing data privacy compliance across GDPR, CCPA, and other regulations with data discovery, consent management, and DSR handling.",
            "use_case": "Audit, Security and Compliance",
            "lifecycle": "growing",
            "services": [
                "Macie", "Glue", "Athena", "S3", "Lambda",
                "StepFunctions", "DynamoDB", "APIGateway", "CloudWatchLogs",
                "CloudTrail", "KMS", "Config", "AuditManager"
            ],
            "stages": ["security", "compliance", "softwaresolutions-customerdata"],
            "business_unit": "Core",
        },
        "EnterpriseCryptoKeyManagement": {
            "description": "Global cryptographic key management service handling millions of keys across multiple regions with HSM backing, strict compliance controls, and automated rotation.",
            "use_case": "Security",
            "lifecycle": "steady_state",
            "services": [
                "KMS", "CloudHSM", "SecretsManager", "Lambda",
                "DynamoDB", "CloudTrail", "CloudWatchLogs", "EventBridge",
                "SNS", "IAMIdentityCenter"
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
                "MediaConvert", "MediaPackage", "S3", "CloudFront",
                "Lambda", "StepFunctions", "SQS", "Rekognition",
                "Comprehend", "CloudWatchLogs", "Elemental"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "BroadcastMediaDistribution": {
            "description": "Broadcast-grade media distribution network handling live and on-demand content for global audiences with multi-region redundancy and DRM protection.",
            "use_case": "Enterprise Applications",
            "lifecycle": "peak_and_plateau",
            "services": [
                "MediaLive", "MediaConnect", "MediaPackage", "S3",
                "CloudFront", "Route53", "WAF", "ShieldAdvanced",
                "CloudWatchLogs", "Lambda", "ApiGateway"
            ],
            "stages": ["softwaresolutions-prod", "softwaresolutions-staging"],
            "business_unit": "SoftwareSolutions",
        },
        "EnterpriseDigitalAssetManagement": {
            "description": "Centralized digital asset management platform for 100+ million assets with AI-powered tagging, version control, rights management, and global distribution.",
            "use_case": "Enterprise Applications",
            "lifecycle": "growing",
            "services": [
                "S3", "DynamoDB", "ElasticSearch", "Rekognition",
                "Comprehend", "Lambda", "EC2", "ECS", "CloudFront",
                "CloudWatchLogs", "StepFunctions", "SQS"
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
                "EC2", "RDS", "DynamoDB", "S3", "Lambda",
                "APIGateway", "Cognito", "CloudFront", "CloudWatchLogs",
                "KMS", "CloudTrail", "Config", "AuditManager"
            ],
            "stages": ["pharma-prod", "pharma-research", "compliance"],
            "business_unit": "Pharma",
        },
        "HealthcareDataInteroperabilityHub": {
            "description": "Interoperability platform connecting healthcare systems via FHIR, HL7, DICOM with real-time transforms, API management, and secure patient data exchange.",
            "use_case": "Enterprise Integration",
            "lifecycle": "growing",
            "services": [
                "APIGateway", "AppSync", "Lambda", "DynamoDB",
                "EC2", "ECS", "SNS", "SQS", "S3", "ElasticSearch",
                "CloudWatchLogs", "KMS", "StepFunctions", "HealthLake"
            ],
            "stages": ["pharma-prod", "pharma-research"],
            "business_unit": "Pharma",
        },
        "MedicalImageProcessingPlatform": {
            "description": "High-performance platform for processing and analyzing medical imaging data (CT, MRI, ultrasound) with AI diagnosis assistance and research capabilities.",
            "use_case": "Machine Learning and AI",
            "lifecycle": "growing",
            "services": [
                "EC2", "S3", "EFS", "SageMaker", "SageMakerInference",
                "Lambda", "Batch", "DynamoDB", "CloudWatchLogs",
                "SNS", "SQS", "KMS", "CloudFront"
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
                "S3", "EC2", "EKS", "Lambda", "SageMaker",
                "Athena", "QuickSight", "CloudWatchLogs", "StepFunctions",
                "Batch", "Glue", "Location"
            ],
            "stages": ["ml-prod", "supplychain-analytics"],
            "business_unit": "MachineLearning",
        },
        "FleetManagementTelematics": {
            "description": "Real-time fleet management system monitoring 10,000+ vehicles with route optimization, predictive maintenance, and driver behavior analytics.",
            "use_case": "Enterprise Integration",
            "lifecycle": "steady_state",
            "services": [
                "IoT", "KinesisDataStreams", "Timestream", "S3",
                "Lambda", "DynamoDB", "SNS", "APIGateway", "CloudWatchLogs",
                "QuickSight", "EMR", "Location"
            ],
            "stages": ["supplychain-logistics", "manufacturing-iot"],
            "business_unit": "SupplyChain",
        },
        "DisasterResponseCoordinationSystem": {
            "description": "Multi-agency disaster response coordination platform with real-time resource tracking, geospatial analytics, and field communication capabilities.",
            "use_case": "Enterprise Applications",
            "lifecycle": "steady_state",
            "services": [
                "Location", "APIGateway", "Lambda", "DynamoDB",
                "IoT", "SNS", "S3", "CloudFront", "CloudWatchLogs",
                "KMS", "ElasticSearch", "StepFunctions"
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
                "CodePipeline", "CodeBuild", "CodeDeploy", "EC2",
                "ECS", "EKS", "S3", "CloudFront", "Lambda",
                "CloudWatchLogs", "CloudTrail", "KMS", "EventBridge", "SNS"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "MultiCloudInfrastructureOrchestration": {
            "description": "Infrastructure-as-Code platform managing resources across AWS, Azure, GCP with centralized governance, drift detection, and compliance enforcement.",
            "use_case": "Management & Governance",
            "lifecycle": "growing",
            "services": [
                "CloudFormation", "SystemsManager", "Lambda", "DynamoDB",
                "S3", "SNS", "SQS", "EventBridge", "CloudWatchLogs",
                "CloudTrail", "Config", "CodePipeline"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
        "EnterpriseServiceMesh": {
            "description": "Global service mesh controlling 1000+ microservices across multiple clusters with traffic management, security, observability, and chaos engineering capabilities.",
            "use_case": "Management & Governance",
            "lifecycle": "growing",
            "services": [
                "EKS", "EC2", "Lambda", "AppMesh", "XRay",
                "CloudWatchLogs", "CloudWatch", "VPC", "Route53",
                "Certificate Manager", "IAM", "ElasticSearch"
            ],
            "stages": ["shared-services"],
            "business_unit": "Core",
        },
    },
}
