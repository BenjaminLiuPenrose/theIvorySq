#Extracting Text from PDF file
#Before you start, install the package of pdfminer via: pip install pdfminer

import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

#Import chatGPT
#check this if you have questions of parameters: https://platform.openai.com/docs/api-reference/completions/create

#openAI API key: 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
#Before you start, install the package of openai via: pip install openai
import os
import openai
openai.api_key = "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"
"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"

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        
        text = fake_file_handle.getvalue()
    
    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text
      
      
def generate_text(prompt):
    model_engine = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[ {"role": "system", "content": "You are a helpful assistant in academic advising, including understanding research opportunities and students' academic recording"},
        {"role": "user", "content": prompt}],
        #prompt=prompt,   #our input
        max_tokens=1000, #limit the lenth of total context including input and output
        n=1,             #How many completions to generate for each prompt.
        stop=None,       #Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
        temperature=0.5, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    )
    return response

#     if response.choices:
#         return response.choices[0].text.strip()
#     else:
#         return None


# App
opportunity_description = extract_text_from_pdf('2023_Research-Professional_Weber-NBER-ad_final.pdf')

question = 'Could you help me summarize the research topic of the following job posting via a list of keywords, and do not inlcude its job requirements, school names and payment, just research field and topics: '

prompt = question + opportunity_description

generated_text = generate_text(prompt)

print(generated_text["choices"][0]["message"]["content"])

print(generated_text)



opportunity_description = extract_text_from_pdf('2023_Research-Professional_Weber-NBER-ad_final.pdf')

question = 'Could you help me summarize the research topic of the following job posting via a list of keywords, and do not inlcude research field, research topics, school names and payment, just job requirements and skill requirements: '

prompt = question + opportunity_description

generated_text = generate_text(prompt)

print(generated_text["choices"][0]["message"]["content"])

print(generated_text)
