class Node:

  def __init__(self):
    self.node_count = 0
    self.node = {}
    self.matmul_count = 0
    self.matmul = []
    self.variable_count = 0
    self.variable = []

  def addNode(self, node_id, device_id, content, lines):
    self.node[node_id] = {
      'device_id': device_id,
      'content': content,
      'lines': lines,
      'grade': 0
    }

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

  def changeGrade(self, node_id, grade):
    self.node[node_id]['grade'] = grade

  def printAll(self):
    for idx, e in enumerate(self.variable):
      print 'Variable[',idx,']'+e['name']+': '+e['value'][0]+', '+e['value'][1]
    for idx, e in enumerate(self.matmul):
      print 'Matmul[',idx,']: '+e['value'][0]+', '+e['value'][1]

