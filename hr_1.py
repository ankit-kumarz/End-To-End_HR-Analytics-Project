from pyresparser import ResumeParser
from docx import Document
from flask import Flask,render_template,redirect,request
import numpy as np
import pandas as pd
import re
from ftfy import fix_text
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

stopw  = set(stopwords.words('english'))

df =pd.read_csv('job_final.csv') 
df['test']=df['Job_Description'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word)>2 and word not in (stopw)]))

app=Flask(__name__)



@app.route('/')
def hello():
    return render_template("model.html")



@app.route("/home")
def home():
    return redirect('/')

@app.route('/submit',methods=['POST'])
def submit_data():
    if request.method == 'POST':
        
        f = request.files['userfile']
        import os
        ext = os.path.splitext(f.filename)[-1].lower()
        temp_path = 'uploaded_resume' + ext
        f.save(temp_path)
        data = None
        try:
            extracted_text = None
            if ext == '.txt':
                # Try utf-8, fallback to latin-1
                try:
                    with open(temp_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                except UnicodeDecodeError:
                    with open(temp_path, 'r', encoding='latin-1') as file:
                        text = file.read()
                extracted_text = text
                doc = Document()
                doc.add_paragraph(text)
                doc.save('temp_text.docx')
                data = ResumeParser('temp_text.docx').get_extracted_data()
                os.remove('temp_text.docx')
            else:
                # Try to extract text from PDF/DOCX using textract for debug
                try:
                    import textract
                    extracted_text = textract.process(temp_path).decode('utf-8', errors='ignore')
                except Exception as textract_err:
                    print('Textract extraction failed:', textract_err)
                    extracted_text = None
                data = ResumeParser(temp_path).get_extracted_data()
            if extracted_text:
                print('\n--- Extracted Text Start ---\n')
                print(extracted_text[:2000])  # Print first 2000 chars for debug
                print('\n--- Extracted Text End ---\n')
        except Exception as e:
            print('Error extracting skills:', e)
            data = {'skills': []}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        resume = data.get('skills', [])
        if not resume or not any(resume):
            error_msg = 'No skills could be extracted from your resume. Please upload a different file or check the format.'
            return render_template('model.html', tables=None, error=error_msg)
        skills = [' '.join(word for word in resume)]
        org_name_clean = skills
        
        def ngrams(string, n=3):
            string = fix_text(string) # fix text
            string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
            string = string.lower()
            chars_to_remove = [")","(",".","|","[","]","{","}","'"]
            rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
            string = re.sub(rx, '', string)
            string = string.replace('&', 'and')
            string = string.replace(',', ' ')
            string = string.replace('-', ' ')
            string = string.title() # normalise case - capital at start of each word
            string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
            string = ' '+ string +' ' # pad names for ngrams...
            string = re.sub(r'[,-./]|\sBD',r'', string)
            ngrams = zip(*[string[i:] for i in range(n)])
            return [''.join(ngram) for ngram in ngrams]
        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
        tfidf = vectorizer.fit_transform(org_name_clean)
        print('Vecorizing completed...')
        
        
        def getNearestN(query):
          queryTFIDF_ = vectorizer.transform(query)
          distances, indices = nbrs.kneighbors(queryTFIDF_)
          return distances, indices
        nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
        unique_org = (df['test'].values)
        distances, indices = getNearestN(unique_org)
        unique_org = list(unique_org)
        matches = []
        for i,j in enumerate(indices):
            dist=round(distances[i][0],2)
  
            temp = [dist]
            matches.append(temp)
        matches = pd.DataFrame(matches, columns=['Match confidence'])
        df['match']=matches['Match confidence']
        df1=df.sort_values('match')
        df2=df1[['Position', 'Company','Location']].head(10).reset_index()
        
        
        
        
        
    #return  'nothing' 
    return render_template('model.html', tables=df2.to_html(classes='job', index=False), titles=['na','Job'])
        
        
        
        
        
if __name__ =="__main__":
    
    
    app.run()