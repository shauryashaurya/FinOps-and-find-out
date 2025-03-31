# FinOps and find out...                                          
                                          
                                          
<html>                                         
	<img src="./images/finops-banner.png" width="90%" align="center" alt="FinOps and find out... , © Shaurya Agarwal" />                                          
</html>                                          
                                        
An indepth exploration of Cost and Usage data across AWS, GCP and Azure.                                           
All data is notional (and generators for the data are included).                                           
                                          
We perform all sorts of analysis, including chargeback, showback and others.                                           
We try to build models to forecast costs by projects, services etc.                                          
Possibly even try our hand at scenario based analysis too.                                        
                                          
                              
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