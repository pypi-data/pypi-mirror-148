from typing import Tuple, Type, Union
from probnode import SureEvent
from probnode.core import *
from probnode.probability import *


def contract(chain: ChainNode) -> ChainNode:
  """Contract a `ChainNode` using fixed patterns (negating, complement, reciprocal,...)

  Args:
      chain (ChainNode): Input ChainNode

  Returns:
      ChainNode: Contracted ChainNode
  """
  if not issubclass(type(chain), ChainNode):
    raise TypeError(f"Chain argument must be subclass of type {ChainNode.__name__}")

  return contract_arbitrary_node_group(type(chain), chain.args)


def contract_arbitrary_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> ChainNode:
  if chain_type is SumNode:
    result = SumNode()
    result.args = contract_arbitrary_sum_node_group(node_list)

  if chain_type is ProductNode:
    result = ProductNode()
    result.args = contract_arbitrary_product_node_group(node_list)
  return result if result is not None else None


def contract_arbitrary_sum_node_group(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:
  node_list = _convert_SureEvent_in_node_list_to_float(node_list)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = _split_float_vs_normal_vs_inverse_nodes(node_list)
  if _is_incontractible(normal_additive_nodes, additive_inverse_nodes):
    return [
        float_value
        ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes

  (normal_additive_nodes, additive_inverse_nodes
   ) = remove_negating_nodes_from_classified_lists(normal_additive_nodes, additive_inverse_nodes)
  if _is_incontractible(normal_additive_nodes, additive_inverse_nodes):
    return [
        float_value
        ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes

  (normal_additive_nodes,
   additive_inverse_nodes) = remove_or_prob_pattern_nodes_from_classified_lists(
       normal_additive_nodes, additive_inverse_nodes
       )
  if _is_incontractible(normal_additive_nodes, additive_inverse_nodes):
    return [float_value] + normal_additive_nodes if float_value != 0 else normal_additive_nodes

  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = remove_complement_nodes_from_classified_lists(
       float_value, normal_additive_nodes, additive_inverse_nodes
       )

  if len(normal_additive_nodes) > 0:
    for idx, node in enumerate(normal_additive_nodes[:]):
      if issubclass(type(node), ChainNode):
        normal_additive_nodes[idx] = contract(node)
  if len(additive_inverse_nodes) > 0:
    for idx, node in enumerate(additive_inverse_nodes[:]):
      invert_node = node.additive_invert()
      if issubclass(type(invert_node), ChainNode):
        additive_inverse_nodes[idx] = contract(invert_node).additive_invert()
  return [
      float_value
      ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes


def _is_incontractible(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> bool:
  return len(additive_inverse_nodes) == 0 or len(normal_additive_nodes) == 0


def _convert_SureEvent_in_node_list_to_float(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:

  def is_SureEvent_node(n: Node) -> bool:
    return n == Node(P(SureEvent()))

  def is_additive_inverse_SureEvent_node(n: Node) -> bool:
    try:
      return n.additive_invert() == Node(P(SureEvent()))
    except AttributeError:
      return False

  def is_reciprocal_SureEvent_node(n: Node) -> bool:
    try:
      return n.reciprocate() == Node(P(SureEvent()))
    except AttributeError:
      return False

  def try_convert_SureEvent_node(n: Node) -> Union[Node, float]:
    if is_SureEvent_node(n) or is_reciprocal_SureEvent_node(n):
      return float(1)
    if is_additive_inverse_SureEvent_node(n):
      return float(-1)
    return n

  return list(map(try_convert_SureEvent_node, node_list))


def _split_float_vs_normal_vs_inverse_nodes(
    node_list: List[Union[float, Node]]
    ) -> Tuple[float, List[Node], List[Node]]:
  float_value = 0.0
  additive_inverse_nodes = []
  normal_additive_nodes = []
  for node in node_list:
    if isinstance(node, (int, float)):
      float_value = float_value + float(node)
    elif issubclass(type(node), AdditiveInverse):
      additive_inverse_nodes.append(node)
    else:
      normal_additive_nodes.append(node)
  return (float_value, normal_additive_nodes, additive_inverse_nodes)


def contract_negating_nodes(sum: SumNode) -> SumNode:
  """If `sum = ...+ P(A) + ... - P(A) +...` , then remove both `P(A)` and `- P(A)` in `sum`

  """
  node_list = _convert_SureEvent_in_node_list_to_float(sum.args)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = _split_float_vs_normal_vs_inverse_nodes(node_list)
  (normal_additive_nodes, additive_inverse_nodes
   ) = remove_negating_nodes_from_classified_lists(normal_additive_nodes, additive_inverse_nodes)
  contracted_sum = SumNode()
  contracted_sum.args = [
      float_value
      ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes
  return contracted_sum


def remove_negating_nodes_from_classified_lists(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  normal_nodes = normal_additive_nodes[:]
  invert_nodes = additive_inverse_nodes[:]
  for inverse_node in invert_nodes[:]:     # P(A) - P(A) = 0
    for normal_node in normal_nodes[:]:
      if inverse_node.additive_invert(
      ) == normal_node and normal_node in normal_nodes and inverse_node in invert_nodes:
        normal_nodes.remove(normal_node)
        invert_nodes.remove(inverse_node)
  return (normal_nodes, invert_nodes)


def contract_complement_nodes(sum: SumNode) -> SumNode:
  """If `sum = ...+ 1 + ... - P(not A) +...` , then replace both `1` and `- P(not A)` with `P(A)` in `sum`
  
    >>> contract_complement_nodes(1.5 - N(P(not A)))
        (0.5 + N(P(A)))
    >>> contract_complement_nodes(1 - N(P(not A)) + N(P(B)))
        (N(P(A)) + N(P(B)))

  """
  node_list = _convert_SureEvent_in_node_list_to_float(sum.args)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = _split_float_vs_normal_vs_inverse_nodes(node_list)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = remove_complement_nodes_from_classified_lists(
       float_value, normal_additive_nodes, additive_inverse_nodes
       )
  contracted_sum = SumNode()
  contracted_sum.args = [
      float_value
      ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes
  return contracted_sum


def remove_complement_nodes_from_classified_lists(
    float_value: float, normal_additive_nodes: List[Node], additive_invert_nodes: List[Node]
    ) -> Tuple[float, List[Node], List[Node]]:
  """Replace complement nodes
        >>> remove_complement_nodes_from_classified_lists( 5,   # float value
                                                          [..., P(B),...], # Normal additive nodes
                                                          [... - P(not A),...]) # Invert additive nodes
            (4, [...,P(A), P(B),...], [...])
  """
  normal_nodes = normal_additive_nodes[:]
  invert_nodes = additive_invert_nodes[:]
  for node in invert_nodes[:]:
    if float_value >= 1:     # 1 - P(A) = P(not A)
      exp_node = node.additive_invert()
      if exp_node.is_pure_node():
        float_value = float_value - 1
        normal_nodes.append(Node(exp_node.exp.invert()))
        invert_nodes.remove(node)
  return (float_value, normal_nodes, invert_nodes)


def contract_or_prob_pattern_nodes(sum: SumNode) -> SumNode:
  """Contract all Or Probability patterns `P(A) + P(B) - P(A and B) = P(A or B)` in `sum`
  
    >>> contract_or_prob_pattern_nodes(1.5 + N(P(A)) - N(P(A and B)) + N(P(B)))
        (0.5 + N(P(A or B)))

  """
  node_list = _convert_SureEvent_in_node_list_to_float(sum.args)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = _split_float_vs_normal_vs_inverse_nodes(node_list)
  (normal_additive_nodes,
   additive_inverse_nodes) = remove_or_prob_pattern_nodes_from_classified_lists(
       normal_additive_nodes, additive_inverse_nodes
       )
  contracted_sum = SumNode()
  contracted_sum.args = [
      float_value
      ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes
  return contracted_sum


def remove_or_prob_pattern_nodes_from_classified_lists(
    normal_additive_nodes: List[Node], additive_invert_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  """Replace Or Probability pattern nodes with `OrProbabilityExpression`
        >>> remove_or_prob_pattern_nodes_from_classified_lists([...P(A), P(B),...], # Normal additive nodes
                                                                [... - P(A and B),...]) # Invert additive nodes
            ([...P(A or B),...], [...])
  """
  normal_nodes = normal_additive_nodes[:]
  invert_nodes = additive_invert_nodes[:]
  and_prob_list = []
  simple_prob_list = []
  for node in normal_nodes[:]:
    if node.is_pure_node():
      simple_prob_list.append(node.exp)
      normal_nodes.remove(node)
  for node in invert_nodes[:]:
    exp_node = node.additive_invert()
    if exp_node.is_pure_node():
      and_prob = exp_node.exp
      if type(and_prob) is AndProbabilityExpression and node in invert_nodes:
        and_prob_list.append(and_prob)
        invert_nodes.remove(node)
  (simple_prob_list, and_prob_list
   ) = replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs(simple_prob_list, and_prob_list)
  normal_nodes += list(map(lambda x: Node(x), simple_prob_list))
  invert_nodes += list(map(lambda x: Node(x).additive_invert(), and_prob_list))
  return (normal_nodes, invert_nodes)


def replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs(
    simple_prob_list: List[BaseProbabilityExpression], and_prob_list: List[AndProbabilityExpression]
    ) -> Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]:
  """Replace expressions in Or Probability pattern with corresponding `OrProbabilityExpression`
        >>> replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([...P(A), P(B),...], [...P(A and B),...])
          ([...P(A or B),...], [...])
  """
  and_exps_list = list(map(lambda x: [x.base_exp, x.aux_exp], and_prob_list))
  for simple_prob in simple_prob_list[:]:
    for idx, and_exps in enumerate(and_exps_list[:]):
      if simple_prob in and_exps:
        and_exps.remove(simple_prob)
        if len(and_exps) == 0:
          simple_prob_list.remove(and_prob_list[idx].aux_exp)
          simple_prob_list.remove(and_prob_list[idx].base_exp)
          simple_prob_list.append(and_prob_list[idx].base_exp | and_prob_list[idx].aux_exp)
          and_prob_list.pop(idx)
        break

  return (simple_prob_list, and_prob_list)


def contract_arbitrary_product_node_group(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:
  node_list = _convert_SureEvent_in_node_list_to_float(node_list)
  (float_value, normal_nodes,
   reciprocal_nodes) = _split_float_vs_normal_vs_reciprocal_nodes(node_list)
  if len(reciprocal_nodes) == 0 or len(normal_nodes) == 0:
    return [float_value] + simplify_expanded_and_prob_exp(
        normal_nodes + reciprocal_nodes
        ) if float_value != 1 else simplify_expanded_and_prob_exp(normal_nodes + reciprocal_nodes)

  (normal_nodes, reciprocal_nodes
   ) = remove_reciprocal_nodes_from_classified_lists(normal_nodes, reciprocal_nodes)
  if len(reciprocal_nodes) == 0 or len(normal_nodes) == 0:
    return [float_value] + reciprocal_nodes + simplify_expanded_and_prob_exp(
        normal_nodes
        ) if float_value != 1 else reciprocal_nodes + simplify_expanded_and_prob_exp(normal_nodes)

  (normal_nodes, reciprocal_nodes
   ) = simplify_conditional_pattern_nodes_from_classified_lists(normal_nodes, reciprocal_nodes)

  normal_nodes = simplify_expanded_and_prob_exp(normal_nodes)

  if len(normal_nodes) > 0:
    for idx, node in enumerate(normal_nodes[:]):
      if issubclass(type(node), ChainNode):
        normal_nodes[idx] = contract(node)
  if len(reciprocal_nodes) > 0:
    for idx, node in enumerate(reciprocal_nodes[:]):
      invert_node = node.additive_invert()
      if issubclass(type(invert_node), ChainNode):
        reciprocal_nodes[idx] = contract(invert_node).additive_invert()
  return [
      float_value
      ] + normal_nodes + reciprocal_nodes if float_value != 1 else normal_nodes + reciprocal_nodes


def _split_float_vs_normal_vs_reciprocal_nodes(
    node_list: List[Union[float, Node]]
    ) -> Tuple[float, List[Node], List[Node]]:
  float_value = 1.0
  reciprocal_nodes = []
  normal_nodes = []
  for node in node_list:
    if isinstance(node, (int, float)):
      float_value = float_value * float(node)
    elif issubclass(type(node), Reciprocal):
      reciprocal_nodes.append(node)
    else:
      normal_nodes.append(node)
  return (float_value, normal_nodes, reciprocal_nodes)


def contract_reciprocated_nodes(product: ProductNode) -> ProductNode:
  """Contract reciprocated nodes `P(A) / P(A) = 1` in `product`
  
    >>> contract_reciprocated_nodes(1.5 * N(P(A)) / N(P(A)) * N(P(B)))
        (1.5 * N(P(B)))

  """
  node_list = _convert_SureEvent_in_node_list_to_float(product.args)
  (float_value, normal_product_nodes,
   reciprocal_nodes) = _split_float_vs_normal_vs_reciprocal_nodes(node_list)
  (normal_product_nodes, reciprocal_nodes
   ) = remove_reciprocal_nodes_from_classified_lists(normal_product_nodes, reciprocal_nodes)
  contracted_product = SumNode()
  contracted_product.args = [
      float_value
      ] + normal_product_nodes + reciprocal_nodes if float_value != 1 else normal_product_nodes + reciprocal_nodes
  return contracted_product


def remove_reciprocal_nodes_from_classified_lists(
    normal_nodes: List[Node], reciprocal_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  for reciproc_node in reciprocal_nodes[:]:     #  P(A) / P(A) = 1
    for normal_node in normal_nodes[:]:
      if reciproc_node.reciprocate(
      ) == normal_node and normal_node in normal_nodes and reciproc_node in reciprocal_nodes:
        normal_nodes.remove(normal_node)
        reciprocal_nodes.remove(reciproc_node)
  return (normal_nodes, reciprocal_nodes)


def contract_conditional_pattern_nodes(product: ProductNode) -> ProductNode:
  """Contract conditional pattern nodes ` P(X and Y) / P(Y) = P(X when Y)` in `product`
  
    >>> contract_conditional_pattern_nodes(1.5 * N(P(A and B)) / N(P(A)) * N(P(B)))
        (1.5 * N(P(B when A)) * N(P(B)))

  """
  node_list = _convert_SureEvent_in_node_list_to_float(product.args)
  (float_value, normal_product_nodes,
   reciprocal_nodes) = _split_float_vs_normal_vs_reciprocal_nodes(node_list)
  (normal_product_nodes,
   reciprocal_nodes) = simplify_conditional_pattern_nodes_from_classified_lists(
       normal_product_nodes, reciprocal_nodes
       )
  contracted_product = SumNode()
  contracted_product.args = [
      float_value
      ] + normal_product_nodes + reciprocal_nodes if float_value != 1 else normal_product_nodes + reciprocal_nodes
  return contracted_product


def simplify_conditional_pattern_nodes_from_classified_lists(
    normal_nodes: List[Node], reciprocal_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:     # P(A ^ B) / P(B) = P(A | B)

  (reciprocals_prob_list, and_prob_list
   ) = _filter_probs_of_reciprocals_and_andprobs_from_nodes(reciprocal_nodes, normal_nodes)
  (reciprocals_prob_list,
   and_prob_list) = replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs(
       reciprocals_prob_list, and_prob_list
       )
  normal_nodes += list(map(lambda x: Node(x), and_prob_list))
  reciprocal_nodes += list(map(lambda x: Node(x).reciprocate(), reciprocals_prob_list))
  return (normal_nodes, reciprocal_nodes)


def _filter_probs_of_reciprocals_and_andprobs_from_nodes(
    reciprocal_nodes: List[ReciprocalNode], normal_nodes: List[Node]
    ) -> Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]:
  """
  Args:
      reciprocal_nodes (List[ReciprocalNode]): Reciprocal nodes
      normal_nodes (List[Node]): Normal nodes

  Returns:
      Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]: 
        Probability expressions from Reciprocal nodes,    
        And-Probability expressions from Normal nodes
  """

  and_prob_list = []
  reciprocals_prob_list = []
  for node in reciprocal_nodes[:]:
    exp_node = node.reciprocate()
    if exp_node.is_pure_node():
      reciprocals_prob_list.append(exp_node.exp)
      reciprocal_nodes.remove(node)
  for node in normal_nodes[:]:
    if node.is_pure_node():
      and_prob = node.exp
      if type(and_prob) is AndProbabilityExpression and node in normal_nodes:
        and_prob_list.append(and_prob)
        normal_nodes.remove(node)

  return (reciprocals_prob_list, and_prob_list)


def replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs(
    reciprocals_prob_list: List[BaseProbabilityExpression],
    and_prob_list: List[AndProbabilityExpression]
    ) -> Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]:
  """Replace conditional pattern nodes `P(A and B) / P(A) = P(B when A)` with corresponding expression 
        >>> replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([...P(A),...], [...P(A and B),...])
          ([...,...], [..., P(B when A)],...)
  """
  for reciprocal_prob in reciprocals_prob_list[:]:
    for idx, and_exps in enumerate(and_prob_list[:]):
      if reciprocal_prob == and_exps.base_exp:     # check if X of P(X) is either A or B of P(A and B)
        reciprocals_prob_list.remove(reciprocal_prob)
        and_prob_list[
            idx
            ] = and_exps.aux_exp // reciprocal_prob     # replace P(A and B) and P(X) with either P(X when A) or P(X when B)
        break
      elif reciprocal_prob == and_exps.aux_exp:
        reciprocals_prob_list.remove(reciprocal_prob)
        and_prob_list[idx] = and_exps.base_exp // reciprocal_prob
        break

  return (reciprocals_prob_list, and_prob_list)


def contract_expanded_and_prob_pattern_nodes(
    product: ProductNode
    ) -> ProductNode:     # P(A and B) = P(A when B) * P(B)
  """Contract expanded And Probability pattern nodes ` P(Y) * P(X when Y) = P(X and Y)` in `product`
  
    >>> contract_expanded_and_prob_pattern_nodes(1.5 * N(P(A when B)) * N(P(B)))
        (1.5 * N(P(B and A)))

  """
  node_list = _convert_SureEvent_in_node_list_to_float(product.args)
  (float_value, normal_product_nodes,
   reciprocal_nodes) = _split_float_vs_normal_vs_reciprocal_nodes(node_list)
  normal_product_nodes = simplify_expanded_and_prob_exp(normal_product_nodes)
  contracted_product = SumNode()
  contracted_product.args = [
      float_value
      ] + normal_product_nodes + reciprocal_nodes if float_value != 1 else normal_product_nodes + reciprocal_nodes
  return contracted_product


def simplify_expanded_and_prob_exp(normal_node_list: List[Node]) -> List[Node]:
  (normal_nodes, conditional_exp_nodes) = split_normal_vs_conditional_exp_nodes(normal_node_list)
  if len(conditional_exp_nodes) == 0:
    return normal_node_list
  (normal_nodes, conditional_exp_nodes) = _replace_product_node_lists_with_equivalent_and_expnodes(
      normal_nodes, conditional_exp_nodes
      )
  return normal_nodes + conditional_exp_nodes


def split_normal_vs_conditional_exp_nodes(
    normal_node_list: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  conditional_exp_nodes = []
  normal_nodes = []
  for node in normal_node_list:
    if node.is_pure_node() and type(node.exp) is ConditionalProbabilityExpression:
      conditional_exp_nodes.append(node)
    else:
      normal_nodes.append(node)
  return (normal_nodes, conditional_exp_nodes)


def _replace_product_node_lists_with_equivalent_and_expnodes(
    normal_nodes: List[Node], conditional_exp_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  for node in normal_nodes[:]:
    if node.is_pure_node():
      node_exp = node.exp
      for idx, conditional_node in enumerate(conditional_exp_nodes[:]):
        conditional_exp = conditional_node.exp
        if type(
            conditional_exp
            ) is ConditionalProbabilityExpression and conditional_exp.condition_exp == node_exp:     # P(A and B) = P(A when B) * P(B)
          conditional_exp_nodes[idx] = Node(
              conditional_exp.subject_exp & conditional_exp.condition_exp
              )
          normal_nodes.remove(node)
          break
  return (normal_nodes, conditional_exp_nodes)
