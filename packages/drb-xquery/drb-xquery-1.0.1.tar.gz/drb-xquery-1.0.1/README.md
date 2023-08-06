# Xquery for DRB
This xquery module allows execute xquery on DRB nodes.

## Using this module
To include this module into your project, the `drb-xquery` module shall be referenced into `requirement.txt` file, or the following pip line can be run:

```commandline
pip install drb-xquery
```



Example for execute a query on xml node:

```python
    node_file = DrbFileFactory().create("/path_xml_file/namefile.xml")
    node = XmlNodeFactory().create(node_file)

    # request node named 2A_Tile_ID with ns as namespace
    query = DrbXQuery("/ns:Level-2A_Tile_ID")
    result = query.execute(node)

```

Result is always a list of value or dynamic context

Example with external variables:

```python
    # create the query from  String   
    query = DrbXQuery("declare variable $x external; "
                     "declare variable $y external := 5; $x+$y")

    list_var = {'x': 9, 'y': 12}

    result = query.execute(node, list_var)

    # result[0] == 21
```

# Limitations and differences with W3C standard

The data() function return only the value of elt

for example :


```
 data(element root {element foo {"child"}, " parent" })
```

return in W3C standard:

```
child parent
```

return in this implementation: 

```
parent
```

The infinity value is allowed for Decimal as for float: In W3C infinity is 
only allowed for float or double.

The type xs:double is identical to xs:float
The type xs:long, xs:short, xs:byte are identical to xs:integer


Other limitations

Some types are not defined like:
    xs:anyURI
    xs:untypedAtomic
    ...

Some functions are not yet implemented like:
    yearMonthDuration
    deep-equal
    remove
    processing-instruction
    exactly-one
    ...

Some expressions are not (yet) implemented like:
    group by 
    order by 
    typeswitch
    treat as
    map and array are not defined too    

# Warning for user using drb java implementation of Xquery

When using positional predicates, you should be aware that the to keyword does not work as you might expect when used in predicates. If you want the first three products, it may be tempting to use the syntax:

```
doc("catalog.xml")/catalog/product[1 to 3]
```
However, this will raise an error[*] because the predicate evaluates to multiple numbers instead of a single one. You can, however, use the syntax:

```
doc("catalog.xml")/catalog/product[position() = (1 to 3)]
```

For compare function the result is only -1,0, 1 , in java thi function return a negative value that can be different to -1
or a positive value that represent a difference between the two string...