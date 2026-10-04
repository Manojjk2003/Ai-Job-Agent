from app.parsers.resume import sections
def test_section_detector_normalizes_common_headings():
 result=sections('SUMMARY\nAbout me\nWORK EXPERIENCE\nDeveloper\nTECHNICAL SKILLS\nPython')
 assert result['summary']=='About me' and result['experience']=='Developer' and result['skills']=='Python'
def test_section_detector_keeps_unheaded_content():assert sections('Plain resume text')['other']=='Plain resume text'
