# CarbonPDF: A QA Dataset for Component-Level Carbon Footprint of Electronic Devices

The embodied carbon of computing systems constitutes a significant portion of their overall greenhouse gas (GHG) emissions. As part of their environmental initiatives and compliance with evolving standards, many companies now disclose the carbon footprints of their products in sustainability reports, often providing a detailed breakdown. However, these reports are typically presented in diverse and unstructured formats, such as text, tables, and graphs embedded in PDF documents. This lack of standardization creates significant challenges in extracting and analyzing component-specific emissions data, limiting comparative assessments and opportunities for targeted carbon reductions.
To address these challenges, we introduce a carbon question-answering (QA) dataset specifically designed to facilitate the extraction and analysis of data from real-world carbon reports of computing products. The dataset features annotated metadata, a variety of numerical reasoning tasks, and structured derivations to ensure accurate processing of fragmented and inconsistent information. This work lays a foundation for training advanced language models to automate the aggregation and standardization of emissions data, enabling deeper analysis and integration into downstream applications, such as carbon analysis tools, to assess and optimize the carbon footprint of Information and Communication Technology (ICT) systems.

## Data

### Dataset Statistics

We construct our dataset using carbon footprint reports of computing products, summarized in **Table: Summary Statistics of the Dataset**.  
We collected **1,746 PDF reports** from the websites of [HP](https://h20195.www2.hp.com/v2/), [Dell](https://www.dell.com/en-us/dt/corporate/social-impact/advancing-sustainability/climate-action/product-carbon-footprints.htm), [Acer](https://www.acer.com/us-en/sustainability/product-carbon-footprint), and [Lenovo](https://www.lenovo.com/us/en/compliance/eco-declaration/). Each file averages approximately **4,000 characters** and spans around **two pages**.  

Using the Python [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/), we parsed and converted the PDF files into text for processing. To handle the diversity in formatting and content across reports, we developed custom **parsers in Python** tailored to extract relevant information accurately. These parsers are designed to identify and retrieve carbon-related data, including the total **product carbon footprint (PCF)** and its percentage breakdown across various manufacturing components.  

Given the variability in report formats between companies, we implemented **multiple parsing strategies** to account for these differences. Regular expressions were a core part of the parsing process, allowing us to match specific text patterns and locate key data within the converted text. This structured approach ensures reliable extraction of values and metadata, enabling us to create a consistent and comprehensive dataset from unstructured PDF reports.

#### Table: Summary Statistics of the Dataset

| Statistics                            | Total |
| ------------------------------------- | ----- |
| Number of Companies                   | 4     |
| Number of Files                       | 1746  |
| Average number of characters per file | 3752  |
| Average number of words per file      | 538   |
| Average number of pages per file      | 1.76  |


We design **four distinct types of numerical reasoning questions** for querying the carbon reports.  
These include **word matching**, **max/min identification**, **top-k ranking**, and **calculation-based derivations**, as detailed in **Table: Question Statistics**.  

- **Word matching** questions involve extracting answers directly from the PDF without requiring calculations, such as the total carbon footprint or the percentage contributions of specific components.  
  These questions primarily test the ability to locate and retrieve exact matches from the text.  

- **Max/min** questions focus on identifying the components with the maximum or minimum carbon footprints, such as determining the highest or lowest contributor to overall emissions and evaluating the system’s capacity for numerical comparison.  

- **Top-k** questions require identifying the top-ranked components based on their carbon footprints, such as the top three contributors.  

- **Calculation-based** questions involve performing arithmetic operations to derive answers, such as calculating the combined carbon footprint of multiple components or determining the percentage contribution of a subset to the total footprint.

#### Table: Distribution of Question Types in the Dataset

| Question Type | Train     | Test     |
| ------------- | --------- | -------- |
| Word Match    | 6400      | 1500     |
| Max/Min       | 1920      | 450      |
| Top 3/5       | 1280      | 300      |
| Calculation   | 5192      | 1238     |
| **Total**     | **14792** | **3488** |


### Dataset Description

Table **Dataset Glossary** provides an overview of the dataset’s fields, sources, and types. The dataset consists of two types of CSV files: a **Product CSV file** in the `product` folder, which contains data extracted from PDF product carbon reports during the data collection step, and **question-answer (QA) CSV files** in the `QA` folder, which include the generated question-answer records.

We define the **product ID**, an incrementing value starting from 1, as the primary key for each product in the Product CSV file and use it as a foreign key in the QA CSV file. The product records contain fields such as product name and total **product carbon footprint (PCF)** that are directly extracted from the reports.

We provide the **file URL**, which directly links to the PDF report, along with an **archive URL** as a backup in case the file URL becomes inaccessible (using [Wayback Machine](https://web.archive.org/) or [Wayback Machine Archiver](https://github.com/agude/wayback-machine-archiver)).

Moreover, we collect manufacturing and component percentages, which vary by company. For example:

- HP reports provide component percentages *relative to the manufacturing carbon footprint*.
- Dell and Acer reports base them on the *PCF*.

This leads to different methods of calculating component carbon footprints:

- For HP, the component footprint is calculated by applying the percentage to the manufacturing footprint.
- For Dell and Acer, it is computed by multiplying the component percentage by the PCF.

The dataset also contains a **validation notes** column, which provides information about the validation process for each data record, such as whether it was validated programmatically or manually.

We divide the dataset into a **training set and a test set**, with an **80/20 split** based on the documents. An example record from the content of the `products.csv` file is shown in **Table: Product Example**.

---

The **question-answer records** include the **product name** field for easy access to questions by product name. Additional fields are generated by running our Python scripts on the Product CSV file. The `question interests` column identifies the component names referred to in the questions and can be used to locate the corresponding ground truth answers.

For example, when generating the evidence index, we focus specifically on the components highlighted in the question interests. Since a question may address multiple components, both the **ground truth answer** and the **program’s final answer** are represented as lists, maintaining the order in which the components appear.

These lists can contain numeric values for percentages or carbon footprints, as well as text values for component names. An example QA record for the same product is shown in **Table: QA Example**.

#### Table: Dataset Glossary

| Field                                      | Source                            | Type             |
| ------------------------------------------ | --------------------------------- | ---------------- |
| **Product CSV File**                       |                                   |                  |
| Product ID                                 | Primary key                       | Numeric          |
| Product name                               | Raw data in the report            | Text             |
| File URL                                   | Raw data from the website         | Text             |
| Archive URL                                | Raw data from the website         | Text             |
| Company name                               | Raw data in the report            | Text             |
| Product type                               | Raw data in the report            | Text             |
| Product carbon footprint (PCF, kg CO₂e)    | Raw data in the report            | Numeric          |
| Manufacturing CO₂e percentage              | Raw data in the report            | Numeric          |
| Chassis & assembly CO₂e percentage         | Raw data in the report            | Numeric          |
| HDD CO₂e percentage                        | Raw data in the report            | Numeric          |
| SSD CO₂e percentage                        | Raw data in the report            | Numeric          |
| Power supply unit CO₂e percentage          | Raw data in the report            | Numeric          |
| Battery CO₂e percentage                    | Raw data in the report            | Numeric          |
| Mainboard and other boards CO₂e percentage | Raw data in the report            | Numeric          |
| Display CO₂e percentage                    | Raw data in the report            | Numeric          |
| Packaging CO₂e percentage                  | Raw data in the report            | Numeric          |
| ODD CO₂e percentage                        | Raw data in the report            | Numeric          |
| External components CO₂e percentage        | Raw data in the report            | Numeric          |
| Others\* CO₂e percentage                   | Raw data in the report            | Numeric          |
| Manufacturing CO₂e                         | Computed with provided percentage | Numeric          |
| Chassis & assembly CO₂e                    | Computed with provided percentage | Numeric          |
| HDD CO₂e                                   | Computed with provided percentage | Numeric          |
| SSD CO₂e                                   | Computed with provided percentage | Numeric          |
| Power supply unit CO₂e                     | Computed with provided percentage | Numeric          |
| Battery CO₂e                               | Computed with provided percentage | Numeric          |
| Mainboard and other boards CO₂e            | Computed with provided percentage | Numeric          |
| Display CO₂e                               | Computed with provided percentage | Numeric          |
| Packaging CO₂e                             | Computed with provided percentage | Numeric          |
| ODD CO₂e                                   | Raw data in the report            | Numeric          |
| External components CO₂e                   | Raw data in the report            | Numeric          |
| Others\* CO₂e                              | Raw data in the report            | Numeric          |
| Validation notes                           | Added during study                | Text             |
| **QA CSV File**                            |                                   |                  |
| Product ID                                 | Foreign key                       | Numeric          |
| Product name                               | Raw data in the report            | Text             |
| Question                                   | Added during study                | Text             |
| Question type                              | Added during study                | Text             |
| Question interests                         | Added during study                | Text             |
| Evidence index and text                    | Added during study                | Numeric and Text |
| Program                                    | Added during study                | Numeric and Text |
| Ground truth answer                        | Added during study                | Numeric and Text |


#### Table: Product Example

| Field                                       | Value                                                                  |
|---------------------------------------------|------------------------------------------------------------------------|
| Product ID                                 | 443                                                                    |
| Product name                               | Latitude 3180                                                         |
| File URL                                   | [https://i.dell.com/sites/csdocuments/CorpComm_Docs/en/carbon-footprint-latitude-3180.pdf](https://i.dell.com/sites/csdocuments/CorpComm_Docs/en/carbon-footprint-latitude-3180.pdf) |
| Archive URL                                | [https://web.archive.org/web/*/https://i.dell.com/sites/csdocuments/CorpComm_Docs/en/carbon-footprint-latitude-3180.pdf](https://web.archive.org/web/*/https://i.dell.com/sites/csdocuments/CorpComm_Docs/en/carbon-footprint-latitude-3180.pdf) |
| Company name                               | Dell                                                                   |
| Product type                               | Laptop                                                                 |
| Product carbon footprint (kg CO₂e)         | 243                                                                    |
| Manufacturing CO₂e percentage              | 85.9                                                                   |
| Chassis & assembly CO₂e percentage         | 3.1                                                                    |
| HDD CO₂e percentage                        | 0                                                                      |
| SSD CO₂e percentage                        | 21.1                                                                   |
| Power supply unit CO₂e percentage          | 7.1                                                                    |
| Battery CO₂e percentage                    | 2.2                                                                    |
| Mainboard and other boards CO₂e percentage | 26.5                                                                   |
| Display CO₂e percentage                    | 25.6                                                                   |
| Packaging CO₂e percentage                  | 0.3                                                                    |
| ODD CO₂e percentage                        | -                                                                      |
| External components CO₂e percentage        | -                                                                      |
| Others* CO₂e percentage                    | -                                                                      |
| Manufacturing CO₂e                         | 208.737                                                                |
| Chassis & assembly CO₂e                    | 7.533                                                                  |
| HDD CO₂e                                   | 0                                                                      |
| SSD CO₂e                                   | 51.273                                                                 |
| Power supply unit CO₂e                     | 17.253                                                                 |
| Battery CO₂e                               | 5.346                                                                  |
| Mainboard and other boards CO₂e            | 64.395                                                                 |
| Display CO₂e                               | 62.208                                                                 |
| Packaging CO₂e                             | 0.729                                                                  |
| ODD CO₂e                                   | -                                                                      |
| External components CO₂e                   | -                                                                      |
| Others* CO₂e                               | -                                                                      |
| Validation notes                           | Automatic verified (within 99%-101% tolerance).                       |


#### Table: QA Example

| Field                   | Value |
|--------------------------|-------|
| Product ID              | 443 |
| Product name            | Latitude 3180 |
| Question                | What are the carbon footprints of mainboard, batteries, manufacturing, and chassis in the Latitude 3180 laptop? |
| Question type           | Calculation |
| Question interests      | Mainboard, Batteries, Manufacturing, Chassis |
| Evidence index and text | `{"[404,417]": "243 kgCO2e +/-", "[2438,2469]": "Mainboard and Other Boards 26.5%", "[2425,2436]": "Battery 2.2%", "[2353,2371]": "Manufacturing 85.9%", "[2373,2395]": "Chassis & Assembly 3.1%"}` |
| Program                 | `total_carbon=243.0`<br>`mainboard_percent=0.265`<br>`mainboard_carbon=total_carbon*mainboard_percent`<br>`batteries_percent=0.022`<br>`batteries_carbon=total_carbon*batteries_percent`<br>`manufacturing_percent=0.859`<br>`manufacturing_carbon=total_carbon*manufacturing_percent`<br>`chassis_percent=0.031`<br>`chassis_carbon=total_carbon*chassis_percent`<br>`answer=[mainboard_carbon,batteries_carbon,manufacturing_carbon,chassis_carbon]` |
| Ground truth answer     | [64.395, 5.346, 208.737, 7.533] |

## Tutorial

In our repository, the `datasets` directory contains the product and QA datasets, organized into `product` and `QA` subdirectories. The product dataset is saved as *products.csv*, while the QA dataset is divided into *train.csv* and *test.csv*.  

The `codes` directory includes scripts organized into subdirectories, each named after a step in the dataset creation process as shown in **Data collection → Question creation → Evidence extraction → Program generation**
. Unless otherwise noted, all scripts are named with the company name as the primary identifier.  

- The `data_collection` directory contains `download` and `parse` subdirectories, which hold scripts for downloading PCF files from company websites and parsing these files, respectively.  
  - In `download`, there are four scripts named *{company name}_download.py*, each designed to download all PDF files from a specific company's PCF site.  
  - Additionally, *download_with_url.py* enables downloading PCF files one by one using URLs listed in *products.csv*.  

- The `question_generation` directory has four subdirectories corresponding to the four question types in **Word Match, Max/Min, Top 3/5, and Calculation**.  
  - Here, *{company name}_pdf.py* extracts raw text from downloaded PCF reports, and *{company name}_pdf_question.py* generates questions using templates.  

- The `evidence_extraction` directory contains scripts for extracting the evidence needed to answer the generated questions.  

- Lastly, the `program_generation` directory includes three types of scripts:  
  - *{company name}.py* generates programs using templates.  
  - *{company name}_gt.py* extracts ground truth answers from *products.csv*.  
  - *{company name}_exec.py* executes the generated programs, comparing results with ground truth to verify program correctness.
