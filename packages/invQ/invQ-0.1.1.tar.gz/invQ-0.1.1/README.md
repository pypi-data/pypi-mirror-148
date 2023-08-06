# invQ

invQ is a Python package to calculate the angles of quaternions with respect to a reference quaternion considering the point group symmetry of the rigid body.

# Quaternion

You may look at [Wikipedia](https://en.wikipedia.org/wiki/Quaternion) for details.

## Contributor
- [Sumitava Kundu](https://github.com/sumitavakundu007/), [IACS, Kolkata](http://www.iacs.res.in/).

## Installation
### Prerequisites
1. [python3 or higher](https://www.python.org/download/releases/3.0/)
2. [rowan](https://pypi.org/project/rowan/)


# Installation via [pip](https://pip.pypa.io/en/stable/)
```bash
pip install pltRDF
```

#### Using source code
```bash
git clone https://github.com/sumitavakundu007/invQ.git
tar -xvf invQ-X.X.X
cd invQ-X.X.X
python3 setup.py install --user
```

## Usage

```python
from invQ import invQuat
invQuat("orientations.json", "equivQ.json")
```
#### You need to prepare 'orientations.json' and 'equivQ.json'

# Sample format for 'orientations.json'
```python
{
    "refQ" : [1, 0, 0, 0],   # The refernce quaternion which you want to use to calculate the angles
    "Orientations" : [[1, 0, 0, 0]]   # The quaternions of the rigid body 
}
```

# Sample format for 'equivQ.json'
```python
{
    "Equivalent_orientations" : [[1, 0, 0, 0]]   # Equivalent quaternions from the point group symmetry of the rigid body.
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/
