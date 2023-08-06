(:*******************************************************:)
(: Test: modules-circular.xq                             :)
(: Written By: Mary Holstege                             :)
(: Date: 2005/12/05 14:46:04                             :)
(: Purpose: Importing circular modules                   :)
(:*******************************************************:)

(: insert-start :)
import module namespace test1="http://www.w3.org/TestModules/test1" at  "tests/files/import/test1-lib.xq";;
declare variable $input-context external;
(: insert-end :)

<result>{test1:ok()}</result>
