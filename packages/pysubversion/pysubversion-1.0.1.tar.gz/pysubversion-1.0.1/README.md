<div id="top"></div>


<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">PySubversion</h3>

  <p align="center">
    SVN command-line client wrapper.
    <br />
    <a href="https://github.com/ryanbender2/pysvn"><strong>Explore the docs</strong></a>
    <br />
    <br />
    <a href="https://github.com/ryanbender2/pysvn/issues">Report Bug</a>
    ---
    <a href="https://github.com/ryanbender2/pysvn/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This client supports the major operations of the svn command-line client. Please put in a feature request if you would like more operations to be added!

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Subversion CLI Client](https://svnbook.red-bean.com/en/1.7/svn.ref.svn.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Installers are available on `Pypi`.

```
python -m pip install --upgrade pysubversion
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

> initialize the client on `cwd`

```python
import pysvn

svn = pysvn.Client()
```

### revert

> Revert a given path + options...

```python
svn.revert('foo.txt')
```

```python
svn.revert('foo/', recursive=True)
```

```python
svn.revert('foo.txt', remove_added=True)
```

### log

> Show the log messages for a set of revision(s) and/or path(s)..

```python
svn.log()
```

```python
svn.log(revision=12)
```

```python
svn.log(revision='1:3')
```

```python
svn.log(file='foo.txt', revision=Revision.HEAD)
```

### diff

> Display local changes or differences between two revisions or paths

```python
svn.diff(1)
```

```python
svn.diff(3, 4)
```

### update

> Bring changes from the repository into the working copy.

```python
svn.update()
```

```python
svn.update(path='foo.txt')
```

```python
svn.update(path=['foo.txt', 'bar.c'])
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the BSD 3-Clause License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ryan Bender - [@itsmeryan.hihello](https://www.instagram.com/itsmeryan.hihello/) - ryan.bender@cfacorp.com

Project Link: [https://github.com/ryanbender2/pysvn](https://github.com/ryanbender2/pysvn)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [leafvmaple](https://github.com/leafvmaple)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ryanbender2/pysvn.svg?style=for-the-badge
[contributors-url]: https://github.com/ryanbender2/pysvn/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ryanbender2/pysvn.svg?style=for-the-badge
[forks-url]: https://github.com/ryanbender2/pysvn/network/members
[stars-shield]: https://img.shields.io/github/stars/ryanbender2/pysvn.svg?style=for-the-badge
[stars-url]: https://github.com/ryanbender2/pysvn/stargazers
[issues-shield]: https://img.shields.io/github/issues/ryanbender2/pysvn.svg?style=for-the-badge
[issues-url]: https://github.com/ryanbender2/pysvn/issues
[license-shield]: https://img.shields.io/github/license/ryanbender2/pysvn.svg?style=for-the-badge
[license-url]: https://github.com/ryanbender2/pysvn/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ryan-bender-20a5a8154/