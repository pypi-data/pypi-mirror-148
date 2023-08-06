(:*******************************************************:)
(: Test: errata8-module3b.xq                             :)
(: Written By: John Snelson                              :)
(: Date: 2009/10/01                                      :)
(: Purpose: Module that imports another module and uses a function from it, testing circular dependencies :)
(:*******************************************************:)

module namespace errata8_3b="http://www.w3.org/TestModules/errata8_3b";
import module namespace errata8_3a="http://www.w3.org/TestModules/errata8_3a"  at "tests/files/import/errata8-module3a.xq";

declare variable $errata8_3b:var := 10;
