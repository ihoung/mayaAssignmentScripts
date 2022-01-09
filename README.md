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

## Parameter
| Parameter        | Description         |
| ---------------- | ------------------- |
| Runtime Mode     | When this mode is on, generation will be applied immediately whenever any parameter changed. Considering the calculation speed, this mode is only recommanded to use when you don't have too many objects generated.|
| Density          | The generation density on terrain surface. |
| Min Scale        | Minimum scale of randomly generated object. |
| Max Scale        | Minimum scale of randomly generated object. |
| Growing Direction| The orientation of the generated objects' up direction. **Up**:  the opposite direction of gravity (-y axis).  **Surface Normal**: the current surface normal.  **Customized**: input the direction you want.  **Natural Growing**: when this checkbox is on, the growing direction is the orientation between up direction and current selected direction.|
| Undo             | Undo the last operation. |
| Accept           | Apply and then close the window. |
| Apply            | To generate objects. In runtime mode, this button is to ensure the current operation, and start a new operation. The previous generated objects won't disappear when any parameter changes if applied in runtime mode. |
| Cancel           | Close the window |
