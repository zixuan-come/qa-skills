"""Validate packaging and synthetic artifacts; does not invoke an AI model."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/address-change'
EXPECTED = {'requirement-review', 'requirement-analysis', 'structured-testcase-design',
            'testcase-evaluation', 'test-report', 'testcase-design', 'resume-fraud-review'}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_artifact(value, skill):
    schema = load(ROOT / f'skills/{skill}/references/output.schema.json')
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)
    if skill in {'requirement-review', 'testcase-evaluation'}:
        if value['decision'] == 'pass' and any(issue['severity'] in {'blocker', 'high'} for issue in value['issues']):
            raise ValueError('A passing review cannot contain unresolved high/blocker issues')
    if skill == 'test-report':
        if value['total_cases'] != sum(value[key] for key in ('passed', 'failed', 'blocked', 'skipped')):
            raise ValueError('Report counts do not add up')


def check_markdown_links():
    count = 0
    for path in ROOT.rglob('*.md'):
        outside_code = []
        fenced = False
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.lstrip().startswith('```'):
                fenced = not fenced
            elif not fenced:
                outside_code.append(line)
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', '\n'.join(outside_code)):
            if link.startswith(('https://', 'http://', 'mailto:', '#')):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                raise ValueError(f'Broken or external local link: {path.relative_to(ROOT)} -> {link}')
            count += 1
    return count


def main():
    skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    assert {path.parent.name for path in skills} == EXPECTED
    names = set()
    for path in skills:
        text = path.read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        assert match, f'Missing frontmatter: {path}'
        frontmatter = yaml.safe_load(match[1])
        name = frontmatter['name']
        assert name == path.parent.name and name not in names
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) and len(name) <= 64
        assert isinstance(frontmatter['description'], str) and frontmatter['description'].strip()
        names.add(name)

    schema_files = list((ROOT / 'skills').rglob('*.schema.json'))
    for path in schema_files:
        Draft202012Validator.check_schema(load(path))

    manifest = {
        'review.json': 'requirement-review', 'review-confirmed.json': 'requirement-review',
        'analysis.json': 'requirement-analysis', 'design-v1.json': 'structured-testcase-design',
        'design-v2-partial.json': 'structured-testcase-design', 'design-approved-demo.json': 'structured-testcase-design',
        'evaluation.json': 'testcase-evaluation', 'report-demo.json': 'test-report',
    }
    for filename, skill in manifest.items():
        validate_artifact(load(EXAMPLES / filename), skill)
    batch = load(EXAMPLES / 'execution-demo.json')
    schema = load(ROOT / 'skills/test-report/references/execution-batch.schema.json')
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(batch)

    analysis = load(EXAMPLES / 'analysis.json')
    requirements = {row['requirement_id'] for row in analysis['requirements']}
    assert len(requirements) == len(analysis['requirements'])
    for filename in ('design-v1.json', 'design-v2-partial.json', 'design-approved-demo.json'):
        design = load(EXAMPLES / filename)
        points = {point['test_point_id'] for point in design['test_points']}
        assert len(points) == len(design['test_points'])
        assert len({case['case_id'] for case in design['test_cases']}) == len(design['test_cases'])
        for point in design['test_points']:
            assert set(point['requirement_refs']) <= requirements
        for case in design['test_cases']:
            assert set(case['requirement_refs']) <= requirements
            assert set(case['test_point_refs']) <= points

    approved = load(EXAMPLES / 'design-approved-demo.json')
    assert batch['test_design_id'] == approved['meta']['artifact_id']
    assert batch['test_design_version'] == approved['meta']['version']
    cases = {case['case_id']: case for case in approved['test_cases']}
    seen = set()
    for record in batch['records']:
        reference = (record['case_id'], record['case_version'])
        assert reference not in seen
        seen.add(reference)
        assert record['case_version'] == cases[record['case_id']]['version']
        for evidence in record['evidence']:
            target = (EXAMPLES / evidence['path']).resolve()
            assert target.is_relative_to(EXAMPLES) and target.is_file()
    report = load(EXAMPLES / 'report-demo.json')
    counts = Counter(row['result'] for row in batch['records'])
    assert report['total_cases'] == len(batch['records'])
    for result in ('passed', 'failed', 'blocked', 'skipped'):
        assert report[result] == counts[result]
    record_ids = {row['record_id'] for row in batch['records']}
    point_ids = {row['test_point_id'] for row in approved['test_points']}
    for trace in report['trace_refs']:
        assert trace['source'] in requirements
        assert set(trace['refs']) <= set(cases) | record_ids | point_ids

    # A few negative checks establish that the validator rejects meaningful errors.
    invalid = []
    bad = deepcopy(approved); bad['test_cases'][0]['priority'] = 'P9'
    invalid.append((bad, 'structured-testcase-design'))
    bad = deepcopy(analysis); bad['requirements'] = []
    invalid.append((bad, 'requirement-analysis'))
    bad = deepcopy(report); bad['passed'] = -1
    invalid.append((bad, 'test-report'))
    bad = deepcopy(report); bad['total_cases'] += 1
    invalid.append((bad, 'test-report'))
    bad = load(EXAMPLES / 'review.json'); bad['decision'] = 'pass'
    invalid.append((bad, 'requirement-review'))
    bad = deepcopy(analysis); bad['unrecognized_field'] = True
    invalid.append((bad, 'requirement-analysis'))
    for value, skill in invalid:
        try:
            validate_artifact(value, skill)
        except (ValidationError, ValueError):
            continue
        raise AssertionError(f'Invalid {skill} artifact was accepted')
    links = check_markdown_links()
    print(f'PASS: {len(skills)} unique skills, {len(schema_files)} schemas, {len(manifest) + 1} JSON examples, {len(invalid)} rejected invalid artifacts, {links} local links; IDs, versions, evidence paths and report counts consistent.')
    print('Static validation only; no model evaluation, real test execution or hiring decision was performed.')


if __name__ == '__main__':
    main()
