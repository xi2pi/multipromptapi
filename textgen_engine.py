# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:14:54 2022

@author: chris

\f = new page
\a = new paragraph

"""


from docxtpl import DocxTemplate
#from pyxml2pdf import xml2pdf 

import pandas as pd
import re
# import random
# import string

import openai



def build_text(text_input):
    # Loading template
    template = DocxTemplate('template_doc.docx')

    
    ##################################################
    ##################################################
    ### Claim processing
    
    text_input_cleared = re.sub(r'\n', '', text_input)
    text_input_cleared = re.sub(r'\n\n', '', text_input_cleared)
    
    data_into_list = text_input_cleared.split('.')
    data_into_list = list(filter(None, data_into_list))
    
    
    command_df = pd.DataFrame({"commands":data_into_list})
    
    
    ##################################################
    ##################################################
    ### OpenAI
    
    ### Set up the OpenAI API client
    openai_output = ''
    
    openai.api_key = "enter your key here"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    
    for j in range(0, len(command_df)):
        prompt = command_df["commands"].iloc[j]
    
        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
    
        response = completion.choices[0].text
        
        openai_output += response 
    
    ##################################################
    ##################################################
    ### Data
    
    _generated_text = openai_output
    
    ##################################################
    ##################################################
    
    #Declare template variables
    context = {
        'generated_text': _generated_text,

        }
    
    
    # Rendering
    template.render(context)
    
    # Saving
    template.save('output_openai.docx')
    
    with open('output_openai.txt', 'w', encoding = 'iso-8859-1') as f:
        f.write(openai_output)
    
    return command_df






