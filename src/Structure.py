""" Node Class Variable                """
"""                                    """
""" node (array)                       """
"""                                    """
""" index is node_id                   """
""" Each Element                       """
""" {                                  """
"""   'content': [source string]       """
"""   'lines': [source lines]          """
"""   'device_id': [device_id]         """
"""   'grade': [grade]                 """
""" }                                  """
"""                                    """
""" variable (array)                   """
"""                                    """
""" Each Element                       """
""" {                                  """
"""   'node_id': [node_id] Belong which node """
"""   'name': [name] Variable name           """
"""   'type': matmul, placeholder ...  """
"""   'value': [None, 100], or [x, y_] """
""" }                                  """
"""                                    """
""" matmul (array)                     """
"""                                    """
""" Each Element                       """
""" {                                  """
"""   'node_id': [node_id] Belong which node """
"""   'variable_id': [variable_id]     """
"""   'value': [None, 100], or [x, y_] """
""" }                                  """


class Node:

  def __init__(self):
    self.node_count = 0
    self.node = []
    self.matmul_count = 0
    self.matmul = []
    self.variable_count = 0
    self.variable = []

  def addNode(self, node_id, device_id, content, lines):
    self.node.append({
      'node_id': node_id,
      'device_id': device_id,
      'content': content,
      'lines': lines,
      'grade': 0
    })

    self.node_count += 1

  def addVariable(self, node_id, name, type, value):
    self.variable.append({
      'node_id': node_id,
      'type': type,
      'name': name,
      'value': value
    })

    if(type == 'matmul'):
      self.addMatmul(node_id, self.variable_count, value)

    self.variable_count += 1

  def addMatmul(self, node_id, variable_id, value):
    self.matmul.append({
      'node_id': node_id,
      'variable_id': variable_id,
      'value': value
    })

    self.matmul_count += 1

  def getMatmul(self, matmul_id, r_array):
    cur = self.matmul[matmul_id]
    variable_id1 = cur['value'][0]['variable_id']
    variable_id2 = cur['value'][1]['variable_id']
    type1 = cur['value'][0]['type']
    type2 = cur['value'][1]['type']

    if(type1 == 'matmul'):
      matmul_id = self.variable[variable_id1]['matmul_id']
      r_array = self.getMatmul(matmul_id, r_array)
    else:
      r_array.append(self.variable[variable_id1]['value'][0])
      r_array.append(self.variable[variable_id1]['value'][1])

    if(type2 == 'matmul'):
      matmul_id = self.variable[variable_id2]['matmul_id']
      r_array = self.getMatmul(matmul_id, r_array)
    else:
      r_array.append(self.variable[variable_id2]['value'][0])
      r_array.append(self.variable[variable_id2]['value'][1])
    return r_array

  def printAll(self):
    for idx, e in enumerate(self.variable):
      print 'Variable[',idx,']'+e['name']+': '+e['value'][0]+', '+e['value'][1]
    for idx, e in enumerate(self.matmul):
      print 'Matmul[',idx,']: '+e['value'][0]+', '+e['value'][1]

