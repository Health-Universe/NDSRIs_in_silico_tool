# Copyright 2023 Novartis Institutes for BioMedical Research Inc.
 
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
 
# https://www.mit.edu/~amini/LICENSE.md
 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
from streamlit_ketcher import st_ketcher
import io
from indigo import *
from CPCA_rules import combine_all_rules_together
from template import create_word_file
import pandas as pd

# Streamlit Application Page Set-up
st.set_page_config(page_title="SMILES Input",layout="wide")
st.write("<style>body { margin-top:0px; margin-right: 10px; margin-bottom: 5px; margin-left: 10px; }</style>", unsafe_allow_html=True)

st.title('Nitrosamine Potency Category')
DEFAULT_MOL = 'CC(C=C(C(F)(F)F)C=C1OCC2=CC=CC=C2)=C1C3=CC=C(N(N=O)[C@@H]4CCCN(C)C4)N=N3'
# molecule = st.text_input("Molecule", DEFAULT_MOL)

col1, col2, col3 = st.columns([2,1,1],gap = 'medium')

with col1:
    molecule = st.text_input("Molecule", DEFAULT_MOL)
    smile_code = st_ketcher(molecule)
    st.markdown(f"Smile code: ``{smile_code}``")
# smiles_input = st.text_input('Enter a SMILES string', '')

with col2:
    if st.button('Calculate the Potency Category'):
        if smile_code:
            mol = Chem.MolFromSmiles(smile_code)
            if not mol:
                indigo = Indigo()
                mol1 = indigo.loadMolecule(smile_code)
                mol1.dearomatize()
                new_smile = mol1.smiles()
                mol = Chem.MolFromSmiles(new_smile)
                smile_code = new_smile
            if mol:
                messages,score = combine_all_rules_together(smile_code)
        # print('\n'.join(messages))
                if score == None or score == 100:
                    category = 'Potency Category 5 : AI = 1500 ng/day'
                elif score >= 4:
                    category = 'Potency Category 4 : AI = 1500 ng/day'
                elif score == 3:
                    category = 'Potency Category 3 : AI = 400 ng/day'
                elif score == 2:
                    category = 'Potency Category 2 : AI = 100 ng/day'
                elif score <= 1:
                    category = 'Potency Category 1 : AI = 18 ng/day'
                for message in messages:
                    st.write(message)
                st.write(f'Score: {score}')
                st.write(category)
        Draw.MolToFile(mol, 'mol.png',size=(600, 600))
        create_word_file('mol.png', 'flowchart.png',messages,score)

with col3:
    st.write('This is flowchart on assigning potency category')

    st.image("flowchart.png", caption='Flow Chart', use_column_width=True)
