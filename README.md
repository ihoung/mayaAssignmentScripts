# Maya scripts for landscape generation
Copy all the python scripts into your default Maya scripts folder.

In Maya Script Editor, input following codes into Python Tab, then execute.
```
import LandscapeGenWnd as lgw
lgw.LandscapeGenWnd().createGenWnd('Landscape Generator')
```

If the window is closed and you want reopen it, please use the following code.
```
reload(lgw)
lgw.LandscapeGenWnd().createGenWnd('Landscape Generator')
```
