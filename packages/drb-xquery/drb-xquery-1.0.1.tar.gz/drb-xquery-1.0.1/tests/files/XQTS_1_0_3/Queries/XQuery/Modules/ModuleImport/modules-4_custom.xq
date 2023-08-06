(:*******************************************************:)
(: Test: modules-4.xq                                    :)
(: Description: Evaluates actual usage of a variable declared in an imported module. :)
(:********************************************************** :)

(: insert-start :)
import module namespace defs="http://www.w3.org/TestModules/defs" at "tests/files/import/moduleDefs-lib.xq";
declare variable $input-context external;
(: insert-end :)

let $var := $defs:var1+ 1
return
  $var
