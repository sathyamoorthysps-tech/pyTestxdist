import xml.etree.ElementTree as ET
import os, csv
jpath='results.xml'
tests=failures=errors=skipped=passed=''
if os.path.exists(jpath):
    try:
        tree=ET.parse(jpath)
        root=tree.getroot()
        # Handle either <testsuite ...> or <testsuites><testsuite .../></testsuites>
        if root.tag == 'testsuite':
            suite = root
            tests = suite.attrib.get('tests','')
            failures = suite.attrib.get('failures','')
            errors = suite.attrib.get('errors','')
            skipped = suite.attrib.get('skipped','')
        elif root.tag == 'testsuites':
            # Sum across nested testsuite elements
            t=f=e=s=0
            for suite in root.findall('testsuite'):
                try:
                    t += int(suite.attrib.get('tests') or 0)
                    f += int(suite.attrib.get('failures') or 0)
                    e += int(suite.attrib.get('errors') or 0)
                    s += int(suite.attrib.get('skipped') or 0)
                except Exception:
                    pass
            tests=str(t); failures=str(f); errors=str(e); skipped=str(s)
        if tests.isdigit():
            passed = str(int(tests)-int(failures or 0)-int(errors or 0)-int(skipped or 0))
    except Exception as e:
        print('Error parsing junit xml:', e)

print('JUnit summary: tests=%s failures=%s errors=%s skipped=%s passed=%s' % (tests,failures,errors,skipped,passed))

# Create metrics CSV
os.makedirs('metrics', exist_ok=True)
fname=os.path.join('metrics', 'metrics_local_win_py312.csv')
with open(fname, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['job','os','python','tests_total','failures','errors','skipped','passed'])
    w.writerow(['test-local','Windows','3.12',tests,failures,errors,skipped,passed])

print('Wrote', fname)
