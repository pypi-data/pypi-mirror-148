module namespace modprefix = "libraryModuleURI";

declare variable $modprefix:var := 20;

declare function modprefix:func ($a as xs:string) as xs:string
{
   $a
};

declare function modprefix:add ($a as xs:integer, $b as xs:integer) as xs:integer
{
  ($a + $b) * 2
};
