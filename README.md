# Resume Screening Assistance ( live link - https://resume-screening-assistance-ai.streamlit.app/ )

![Python](https://img.shields.io/badge/python-v3.10-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-v3.5-blue)
![Pinecone Vector Database](https://img.shields.io/badge/Pinecone-Vector%20Database-green)
![LangChain](https://img.shields.io/badge/LangChain-Icon-green)
![Streamlit](https://img.shields.io/badge/streamlit-v1.0.0-green)



This Streamlit application assists in the resume screening process by analyzing job descriptions and resumes. It uses Pinecone for vector storage and OpenAI for embeddings and summarization.

## Features

- **Upload Resumes**: Easily upload multiple PDF resumes for analysis.
- **Job Description Input**: Paste the job description to find relevant resumes.
- **Customized Analysis**: Receive a specified number of relevant resumes based on the job description.
- **Summarization**: Quickly review each relevant resume with a summarized overview.
- **Vector Storage**: Efficiently store document vectors using Pinecone for easy retrieval.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/samad-ms/Resume_Screening_Assistance_AI.git
   ```

2. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your OpenAI API key, To get the key go to - https://platform.openai.com/api-keys
   **Configure your pinecone API key and Index Name, To get the key go to - https://www.pinecone.io/

python config.py
Enter Your OpenAI API KEY when prompted. Your key will be saved to secrets.toml.
Enter Your pinecone API KEY when prompted. Your key will be saved to secrets.toml.
Enter Your PINECONE_INDEX_NAME when prompted. Your key will be saved to secrets.toml.

## Usage

1. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please feel free to open a pull request or an issue.

## License

This project is licensed under the MIT License
