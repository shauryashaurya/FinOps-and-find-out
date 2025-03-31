"""
Multi-Cloud Configuration File

This file defines multi-cloud project configurations for data generation.
"""

MULTI_CLOUD_PROJECTS = {
    "FinancialServicesHybrid": {
        "description": "Core banking systems in AWS with analytical workloads in Azure",
        "use_case": "Enterprise Applications",
        "business_unit": "Finance",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "RDS", "Lambda", "DynamoDB", "EFS", "DirectConnect", "EBS", "SecretsManager", "KMS"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.7
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "SynapseAnalytics", "SQLDatabase", "DataFactory", "BlobStorage", "MachineLearning"
                ],
                "stages": [
                    "ml-prod", "ml-analytics"
                ],
                "percentage": 0.3
            }
        }
    },

    "RetailPlatformMigration": {
        "description": "E-commerce retail platform migrating from AWS to GCP",
        "use_case": "Enterprise Applications",
        "business_unit": "Retail",
        "multi_cloud_pattern": {
            "type": "migration",
            "params": {
                "source_cloud": "aws",
                "target_cloud": "gcp",
                "start_ratio": 0.3,  # Migration starts 30% into the timeline
                "duration_ratio": 0.4  # Migration takes 40% of the timeline
            }
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "declining",
                "services": [
                    "EC2", "RDS", "ElastiCache", "S3", "CloudFront", "Route53", "EBS", "ELB"
                ],
                "stages": [
                    "supplychain-prod", "supplychain-staging"
                ],
                "percentage": 0.8  # Initial percentage before migration
            },
            "gcp": {
                "base_lifecycle": "growing",
                "services": [
                    "ComputeEngine", "CloudSQL", "Memorystore", "CloudStorage", "CloudCDN", "CloudDNS", "PersistentDisk", "CloudLoadBalancing"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.2  # Initial percentage before migration
            }
        }
    },

    "HealthcareTriCloudAnalytics": {
        "description": "Healthcare analytics platform leveraging services across AWS, GCP, and Azure",
        "use_case": "Data Processing and ETL",
        "business_unit": "Healthcare",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "RDS", "S3", "Lambda", "Glue", "Athena"
                ],
                "stages": [
                    "pharma-prod", "pharma-research"
                ],
                "percentage": 0.4
            },
            "gcp": {
                "base_lifecycle": "steady_state",
                "services": [
                    "BigQuery", "VertexAI", "CloudStorage", "Dataflow", "Pub/Sub"
                ],
                "stages": [
                    "ml-prod", "ml-analytics", "ml-featurestore"
                ],
                "percentage": 0.3
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "MachineLearning", "SynapseAnalytics", "CognitiveServices", "DataFactory"
                ],
                "stages": [
                    "ml-prod", "ml-staging", "pharma-research"
                ],
                "percentage": 0.3
            }
        }
    },

    "CloudExpansionMediaServices": {
        "description": "Media processing platform expanding from AWS to Azure",
        "use_case": "Enterprise Applications",
        "business_unit": "Media",
        "multi_cloud_pattern": {
            "type": "expansion",
            "params": {
                "new_cloud": "azure",
                "start_ratio": 0.25,  # Expansion starts 25% into the timeline
                "duration_ratio": 0.4  # Expansion takes 40% of the timeline
            }
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "S3", "MediaConvert", "MediaLive", "CloudFront", "ElasticSearch", "Lambda"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.95  # Initial percentage before expansion
            },
            "azure": {
                "base_lifecycle": "growing",
                "services": [
                    "VirtualMachines", "BlobStorage", "MediaServices", "LiveVideo", "CDN", "ElasticSearch", "Functions"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.05  # Initial percentage before expansion
            }
        }
    },

    "MultiCloudConsolidation": {
        "description": "IT operations consolidating from three clouds to AWS",
        "use_case": "Management & Governance",
        "business_unit": "IT",
        "multi_cloud_pattern": {
            "type": "consolidation",
            "params": {
                "removed_cloud": "gcp",
                "target_cloud": "aws",
                "start_ratio": 0.4,  # Consolidation starts 40% into the timeline
                "duration_ratio": 0.3,  # Consolidation takes 30% of the timeline
                "workload_ratio": 0.3  # Relative size of workload being transferred
            }
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "growing",
                "services": [
                    "EC2", "RDS", "CloudWatch", "Systems Manager", "CloudTrail", "IAM", "GuardDuty", "Config"
                ],
                "stages": [
                    "shared-services", "security"
                ],
                "percentage": 0.5  # Initial percentage before consolidation
            },
            "gcp": {
                "base_lifecycle": "declining",
                "services": [
                    "ComputeEngine", "CloudSQL", "CloudMonitoring", "CloudLogging", "SecurityCommandCenter"
                ],
                "stages": [
                    "shared-services", "security"
                ],
                "percentage": 0.3  # Initial percentage before consolidation
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "VirtualMachines", "SQLDatabase", "Monitor", "LogAnalytics", "DefenderForCloud"
                ],
                "stages": [
                    "shared-services", "security"
                ],
                "percentage": 0.2  # Won't be affected by the consolidation
            }
        }
    },

    "DisasterRecoverySetup": {
        "description": "Manufacturing systems with Azure primary and AWS DR",
        "use_case": "Enterprise Applications",
        "business_unit": "Manufacturing",
        "multi_cloud_pattern": {
            "type": "dr_scenario",
            "params": {
                "primary_cloud": "azure",
                "dr_cloud": "aws",
                "test_frequency_days": 90,  # DR test every 90 days
                "test_duration_days": 3,  # DR test lasts 3 days
                "failover_day": 180,  # Optional failover event on day 180
                "failover_duration_days": 5  # Failover lasts 5 days
            }
        },
        "clouds": {
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "VirtualMachines", "SQLDatabase", "VirtualNetwork", "VPNGateway", "AppService", "EventHubs", "Monitor"
                ],
                "stages": [
                    "manufacturing-prod", "manufacturing-staging"
                ],
                "percentage": 0.9  # Main production environment
            },
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "RDS", "VPC", "VPN", "Lambda", "Kinesis", "CloudWatch"
                ],
                "stages": [
                    "manufacturing-iot", "manufacturing-prod"
                ],
                "percentage": 0.1  # DR environment with minimal standby resources
            }
        }
    },

    "BurstingDevelopmentPlatform": {
        "description": "Development platform with GCP primary and AWS for bursting capacity",
        "use_case": "Developer Tools",
        "business_unit": "Engineering",
        "multi_cloud_pattern": {
            "type": "burst_scaling",
            "params": {
                "primary_cloud": "gcp",
                "burst_cloud": "aws",
                "threshold": 0.8,  # Burst when primary reaches 80% capacity
                "frequency_days": 30,  # Simulate bursts every 30 days
                "duration_days": 5,  # Bursts last 5 days
                "overflow_factor": 0.6  # Burst cloud handles 60% of overflow
            }
        },
        "clouds": {
            "gcp": {
                "base_lifecycle": "steady_state",
                "services": [
                    "ComputeEngine", "CloudBuild", "CloudStorage", "Container Registry", "CloudRun", "CloudSQL"
                ],
                "stages": [
                    "softwaresolutions-dev", "ml-dev"
                ],
                "percentage": 0.8  # Primary development platform
            },
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "CodeBuild", "S3", "ECR", "Lambda", "RDS"
                ],
                "stages": [
                    "sandbox-central", "development"
                ],
                "percentage": 0.2  # Burst capacity platform
            }
        }
    },

    "CloudRepatriationProject": {
        "description": "Finance applications moving from cloud back to on-premises",
        "use_case": "Enterprise Applications",
        "business_unit": "Finance",
        "multi_cloud_pattern": {
            "type": "cloud_repatriation",
            "params": {
                "cloud_source": "aws",
                "start_ratio": 0.3,  # Repatriation starts 30% into the timeline
                "duration_ratio": 0.4  # Repatriation takes 40% of the timeline
            }
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "declining",
                "services": [
                    "EC2", "RDS", "EBS", "EFS", "S3", "VPC", "DirectConnect", "CloudWatch"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 1.0  # Full cloud before repatriation
            }
        }
    },

    "AIMLMultiCloudOptimization": {
        "description": "AI/ML platform choosing optimal services across clouds",
        "use_case": "Machine Learning and AI",
        "business_unit": "Research",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "SageMaker", "SageMakerInference", "S3", "Lambda", "EC2"
                ],
                "stages": [
                    "ml-prod", "ml-staging"
                ],
                "percentage": 0.4  # ML training and large-scale inference
            },
            "gcp": {
                "base_lifecycle": "steady_state",
                "services": [
                    "VertexAI", "AIProtagonist", "BigQuery", "DataFlow", "CloudStorage"
                ],
                "stages": [
                    "ml-featurestore", "ml-analytics"
                ],
                "percentage": 0.4  # Data processing and LLM capabilities
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "MachineLearning", "OpenAI", "CognitiveServices", "Functions", "SynapseAnalytics"
                ],
                "stages": [
                    "ml-dev", "ml-prod"
                ],
                "percentage": 0.2  # Specialized cognitive services
            }
        }
    },

    "MicroservicesMigration": {
        "description": "Microservices architecture migrating from on-prem to multi-cloud",
        "use_case": "Enterprise Applications",
        "business_unit": "Product",
        "multi_cloud_pattern": {
            "type": "expansion",
            "params": {
                "new_cloud": "gcp",
                "start_ratio": 0.1,  # Expansion starts 10% into the timeline
                "duration_ratio": 0.5  # Expansion takes 50% of the timeline
            }
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "Lambda", "DynamoDB", "APIGateway", "S3", "CloudFront", "SQS", "SNS"
                ],
                "stages": [
                    "supplychain-staging", "supplychain-prod"
                ],
                "percentage": 0.8  # Initial percentage before expansion
            },
            "gcp": {
                "base_lifecycle": "growing",
                "services": [
                    "CloudRun", "CloudFunctions", "Firestore", "ApiGateway", "CloudStorage", "CloudCDN", "Pub/Sub"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.2  # Initial percentage before expansion
            }
        }
    },

    "IoTDataPipeline": {
        "description": "Global IoT data pipeline across AWS and Azure",
        "use_case": "Data Processing and ETL",
        "business_unit": "IoT",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "IoT", "Kinesis", "Lambda", "S3", "DynamoDB", "Timestream"
                ],
                "stages": [
                    "manufacturing-iot", "manufacturing-analytics"
                ],
                "percentage": 0.55
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "IoTHub", "EventHubs", "Functions", "BlobStorage", "CosmosDB", "DataFactory", "MachineLearning"
                ],
                "stages": [
                    "manufacturing-iot", "manufacturing-analytics"
                ],
                "percentage": 0.45
            }
        }
    },

    "SecurityComplianceMultiCloud": {
        "description": "Centralized security and compliance spanning all cloud platforms",
        "use_case": "Audit, Security and Compliance",
        "business_unit": "Security",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "GuardDuty", "SecurityHub", "Config", "CloudTrail", "IAM", "KMS", "Inspector"
                ],
                "stages": [
                    "security", "compliance"
                ],
                "percentage": 0.35
            },
            "gcp": {
                "base_lifecycle": "steady_state",
                "services": [
                    "SecurityCommandCenter", "CloudLogging", "IAM", "KeyManagementService", "SecurityLake"
                ],
                "stages": [
                    "security", "compliance"
                ],
                "percentage": 0.3
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "DefenderForCloud", "LogAnalytics", "ActiveDirectory", "KeyVault", "Monitor"
                ],
                "stages": [
                    "security", "compliance"
                ],
                "percentage": 0.35
            }
        }
    },

    "HealthcareExpansion": {
        "description": "Healthcare platform expanding from Azure to AWS",
        "use_case": "Enterprise Applications",
        "business_unit": "Healthcare",
        "multi_cloud_pattern": {
            "type": "expansion",
            "params": {
                "new_cloud": "aws",
                "start_ratio": 0.2,  # Expansion starts 20% into the timeline
                "duration_ratio": 0.4  # Expansion takes 40% of the timeline
            }
        },
        "clouds": {
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "VirtualMachines", "SQLDatabase", "BlobStorage", "HealthDataServices", "AppService", "CognitiveServices"
                ],
                "stages": [
                    "pharma-prod", "pharma-staging"
                ],
                "percentage": 0.95  # Initial percentage before expansion
            },
            "aws": {
                "base_lifecycle": "growing",
                "services": [
                    "EC2", "RDS", "S3", "HealthLake", "Lambda", "Comprehend"
                ],
                "stages": [
                    "pharma-research", "pharma-analytics"
                ],
                "percentage": 0.05  # Initial percentage before expansion
            }
        }
    },

    "GCPToAzureMigration": {
        "description": "E-learning platform migrating from GCP to Azure",
        "use_case": "Enterprise Applications",
        "business_unit": "Education",
        "multi_cloud_pattern": {
            "type": "migration",
            "params": {
                "source_cloud": "gcp",
                "target_cloud": "azure",
                "start_ratio": 0.2,  # Migration starts 20% into the timeline
                "duration_ratio": 0.5  # Migration takes 50% of the timeline
            }
        },
        "clouds": {
            "gcp": {
                "base_lifecycle": "declining",
                "services": [
                    "ComputeEngine", "CloudSQL", "CloudStorage", "CloudCDN", "CloudRun", "Pub/Sub"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.9  # Initial percentage before migration
            },
            "azure": {
                "base_lifecycle": "growing",
                "services": [
                    "VirtualMachines", "SQLDatabase", "BlobStorage", "CDN", "Functions", "EventHubs"
                ],
                "stages": [
                    "softwaresolutions-prod", "softwaresolutions-staging"
                ],
                "percentage": 0.1  # Initial percentage before migration
            }
        }
    },

    "FinancialAnalyticsPlatform": {
        "description": "Financial analytics platform with AWS compute and GCP analytics",
        "use_case": "Data Processing and ETL",
        "business_unit": "Finance",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "EC2", "RDS", "ElastiCache", "S3", "Lambda", "StepFunctions"
                ],
                "stages": [
                    "supplychain-prod", "softwaresolutions-prod"
                ],
                "percentage": 0.6
            },
            "gcp": {
                "base_lifecycle": "steady_state",
                "services": [
                    "BigQuery", "Dataflow", "Dataproc", "CloudStorage", "VertexAI", "Looker"
                ],
                "stages": [
                    "ml-analytics", "softwaresolutions-analytics"
                ],
                "percentage": 0.4
            }
        }
    },

    "HybridDataLakehouse": {
        "description": "Multi-cloud data lakehouse with storage in AWS and compute in Azure",
        "use_case": "Data Processing and ETL",
        "business_unit": "Data",
        "multi_cloud_pattern": {
            "type": "steady_state",
            "params": {}
        },
        "clouds": {
            "aws": {
                "base_lifecycle": "steady_state",
                "services": [
                    "S3", "Glacier", "Athena", "Lake Formation", "Glue", "Lambda"
                ],
                "stages": [
                    "ml-featurestore", "shared-services"
                ],
                "percentage": 0.45
            },
            "azure": {
                "base_lifecycle": "steady_state",
                "services": [
                    "SynapseAnalytics", "DataFactory", "HDInsight", "MachineLearning", "Functions"
                ],
                "stages": [
                    "ml-prod", "ml-staging"
                ],
                "percentage": 0.55
            }
        }
    }
}
