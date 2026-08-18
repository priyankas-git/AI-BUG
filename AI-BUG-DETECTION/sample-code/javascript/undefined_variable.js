function calculateTotal(price, tax) {
  // Bug: Undefined variable assignment (referencing 'taxtotal' instead of 'taxTotal')
  let taxTotal = price * tax;
  return price + taxtotal; 
}
