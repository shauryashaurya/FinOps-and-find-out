# FinOps and find out: **Cost and Usage Data Generators**                                                        
                                                    
                                                    
<html>                                                   
	<img src=".././images/finops-data-generators.webp" width="90%" align="center" alt="FinOps and find out...Data Generators , © 2025, Shaurya Agarwal" />                                                    
</html>                                                    
                                                  
To begin the analysis, we first need to generate _realistic_ looking data.                                                   
We could also use real (anonymized) cost and usage data from actual projects, but this exercise gives us an insight into the idiosyncracies of each cloud service and we can maybe begin to anticipate the changes when dealing with actual projects.          
                                                    
                                        
# Data, Data Dictionaries, Comparisions and Data Generators                      
                    
The repo has minimal data for each (as I want to avoid getting into GitHub LFS).                      
Fork/download the repo and run the data generators.                    
Every generator has a ```DATA_VOLUME_SETTINGS``` dict that can be configured to generate more projects.                     
Each of the generators has a `_config.py` where more details about the services, the projects, account hierarchies etc. can be configured as well.                    
                       
* [AWS](https://github.com/shauryashaurya/FinOps-and-find-out/tree/main/cost-and-usage-data/aws)                                        
* [GCP](https://github.com/shauryashaurya/FinOps-and-find-out/tree/main/cost-and-usage-data/gcp)                                        
* [Azure](https://github.com/shauryashaurya/FinOps-and-find-out/tree/main/cost-and-usage-data/azure)                              
* [**Multi-Cloud** Setup (a mix of GCP, Azure and AWS)](https://github.com/shauryashaurya/FinOps-and-find-out/tree/main/cost-and-usage-data/multi) - this uses the data generators from the AWS, GCP and Azure modules. This was incredibly complex, and frankly a bit frustrating to build - I can totally relate to the FinOps teams dealing with multiple cloud based environments at the same time, esp. in large enterprises... Once this code worked, it was so much fun! :) :) :)                    
                    
                              
                              
                              
.