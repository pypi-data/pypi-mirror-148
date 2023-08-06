# Introduction how to use `resparser`

## Install resparser
`pip insatll resparser`
and `from resparser import resumeparser`

<p>You just need to pass text to `resumeparser` function  </p>

<p>Example:
`from resparser import resumeparser`

#provide your text resume 
`with open(r"C:\Projects\Resume\Resume_Parser\output\1.txt", 'r') as f:   
    data = f.read()`
`resumeparser(data)`

</p>