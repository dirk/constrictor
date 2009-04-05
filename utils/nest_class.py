def nest_class(parent, child):
  setattr(parent, child.__name__, child)
  setattr(child, parent.__name__, parent)
  child._parent = parent