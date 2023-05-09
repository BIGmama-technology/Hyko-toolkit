"""
This file contains dummy task-plans (List[Dict]) representing
the output of the zero-shot-task-planner
"""

test_task_plan_1 = [{'task_id': '1',
  'task': 'image-captioning',
  'task_description': 'Generate a caption for an input image.',
  'dep': [],
  'inputs': [{'id': '1',
    'input_type': 'image',
    'input_description': 'The input image.'}],
  'outputs': [{'id': '2',
    'output_type': 'text',
    'output_description': 'The output caption.'}]},
 {'task_id': '2',
  'task': 'text-to-speech',
  'task_description': 'Generate an audio file of a given caption.',
  'dep': ['1'],
  'inputs': [{'id': '2',
    'input_type': 'text',
    'input_description': 'The input caption.'}],
  'outputs': [{'id': '3',
    'output_type': 'audio',
    'output_description': 'The output pronunciation of the caption.'}]}]

test_task_plan_2 = [{'task_id': 't1',
  'task': 'Convert regulations into searchable format',
  'task_description': 'Transform the existing regulations into a searchable format (e.g. text, pdf, etc.) that can be easily queried by other tasks',
  'dep': [],
  'inputs': [{'id': 'i1',
    'input_type': 'pdf',
    'input_description': 'Existing regulations in PDF format'}],
  'outputs': [{'id': 'o1',
    'output_type': 'text',
    'output_description': 'Regulations in searchable text format'}]},
 {'task_id': 't2',
  'task': 'Retrieve relevant regulations',
  'task_description': "Find the relevant regulations, paragraphs, and articles based on the user's request",
  'dep': ['t1'],
  'inputs': [{'id': 'i2',
    'input_type': 'text',
    'input_description': "User's request text"}],
  'outputs': [{'id': 'o2',
    'output_type': 'text',
    'output_description': 'List of relevant regulations, paragraphs, and articles in text format'}]},
 {'task_id': 't3',
  'task': 'Check for conflicts',
  'task_description': "Identify potential conflicts between the existing regulations and the user's request",
  'dep': ['t2'],
  'inputs': [{'id': 'i3_1',
    'input_type': 'text',
    'input_description': "User's request text"},
   {'id': 'i3_2',
    'input_type': 'text',
    'input_description': 'List of relevant regulations, paragraphs, and articles in text format from task 2'}],
  'outputs': [{'id': 'o3_1',
    'output_type': 'text',
    'output_description': 'List of potential conflicts in text format'},
   {'id': 'o3_2',
    'output_type': 'text',
    'output_description': 'Explanation of each conflict in text format'}]}]

test_task_plan_3 = [{'task_id': 1,
  'task': 'text-to-text generation',
  'task_description': "Generate poem from the user's input text",
  'dep': [],
  'inputs': [{'id': 1,
    'input_type': 'text',
    'input_description': "User's input text"}],
  'outputs': [{'id': 2,
    'output_type': 'text',
    'output_description': 'Generated poem'}]},
 {'task_id': 2,
  'task': 'text-classification',
  'task_description': 'Classify the generated poem as positive or negative emotion',
  'dep': [1],
  'inputs': [{'id': 2,
    'input_type': 'text',
    'input_description': 'Generated poem'}],
  'outputs': [{'id': 3,
    'output_type': 'text',
    'output_description': 'Positive or negative emotion classification result'}]}]
