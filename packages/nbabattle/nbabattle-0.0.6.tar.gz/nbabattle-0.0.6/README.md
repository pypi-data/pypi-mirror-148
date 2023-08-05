![](src/nbabattle/demo/demo.png)
# Generate NBA battle Picture Generator
A lightweight python library to generate two nba team battle image.


## Installation
```shell
$ pip install nbabattle
```

## Usage
```python
from nbabattle import NbaBattle

Photo = NbaBattle('GSW', 'DET')
battle = Photo.create_battle_image()
# Show an image
battle.show()
# Save to the folder
battle.save("generate/gsw-det.png")
```

### Notice
Please use the team's abbreviation as the input.
