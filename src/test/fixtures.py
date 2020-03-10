import pytest


@pytest.fixture()
def simple_aws_event():
    return {
        "awslogs": {
            "data": "H4sIAAAAAAAAAKVSy27bMBD8FYHo0YrIpcSHbw6sBgHitrBUoEViBJS0cgXo4Uh00yTwv3flpGiPLXqdGc4Mh3xhHU6T22P+dEC2ZOtVvrrfpFm2ukrZgg2PPY4ES5loACkUmITgdthfjcPxQEzkHqeodV1Rucjj5MNv3h/CER9eZZkf0XWkAy5sxG0EMrp9d7PK0yzf8VigjiUvVWXjhKsCilIXYIuKgzBcksV0LKZybA6+Gfr3TetxnNjylt2cA1/N70fXV0PHdufA9Dv2fta8sKaam8fWJsJITeWFVGBBgUiE0IRKKxOQXCdKax0La2TMuYyN0cpQtm9oG+86uqZIlAVppBCC88Wvzcg+/bAOtvhwJOF1tQyshhokqhBrV4SxsTo03PFQQGFq48AIy+96dlr8Xzv7l+226aeP2/yfC/r1cXTz4suADC84D7rpzl82bYtV8JuDN2KD3TA+BVnzjHQATLC5JND9CN6IzxNSsk7O+HXf+D88qPoFN2ebu/7LdvU1yEdX4lxVhElljKtAha7WKMraKFqp5LQAbYJYUdMM9x09+KwHdFbGJRdS6pi+FpG0Tjtn166dcE5gp93pJy17fMXzAgAA"
        }
    }
