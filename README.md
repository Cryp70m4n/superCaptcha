# superCaptcha
Super Captcha Beta version 1.0
==========================
**SPECIAL THANKS TO:**
- [YmL](https://github.com/NotYmL) for helping with client-side and testing
- Seva for helping around basic geometry/trigonometry

__ROADMAP__
==========================
**Currently project has no roadmap since it is only beta but it could change in future if project shows to work well in practice.**


__USAGE__
==========================
**The way to solve captcha is to enter the number which inside the biggest triangle on the picture and that is separated from other numbers.**

- POST on /captcha/generate returns json which looks like this {"responseCode": 0, "img": "base64 image", "tag": "random tag"}
- POST on /captcha/solve with json data which contains your tag and answer something like {"tag": "tag", "answer": 42}


__EXAMPLE__
==========================
__You can find example frontend we used for these picutres inside example/frontend directory__
![alt text](https://github.com/Cryp70m4n/superCaptcha/blob/master/samples/captcha.png)
![alt text](https://github.com/Cryp70m4n/superCaptcha/blob/master/samples/correct.png)
![alt text](https://github.com/Cryp70m4n/superCaptcha/blob/master/samples/incorrect.png)



__NOTES__
==========================
*This is only proto-type and if it shows to work well project will be rewritten in RUST for full release.*


__TODO__
==========================
- Improve README
- Write tests
- Write installation script
- Improve comments
- Write documentation for current codebase


__INSTALLATION__
==========================
.. code::
    
    git clone https://github.com/cryp70m4n/superCaptcha

Edit config.ini with your configs and you are ready to go


__REQUIREMENTS__
==========================
- Python version 3.9+
- Python modules: flask, redis, pillow, binascii and cachetools
- Redis

.. code::

    pip3 install flask redis pillow cachetools binascii




__Want to help the project?__
==========================
- For bug reports please open github issue and provide as much details as possible (System, error, use-case, technologies you are trying to use with superCaptcha,...)
- Code commits and improvements are more than welcome just open pull request, just keep in mind to explain reasoning behind changes.


__QUESTIONS?__
==========================
**If you have any questions regarding superCaptcha project feel free to send me an email: cryp70m4n@gmail.com**
