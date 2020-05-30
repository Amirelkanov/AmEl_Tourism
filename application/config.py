class Config(object):
    # Init debug status
    DEBUG = False

    # Init secret key
    SECRET_KEY = 'AmEl-Tourism-key'

    # Init recaptcha
    RECAPTCHA_PUBLIC_KEY = "6Leg2OkUAAAAANYckFuHF37iwk-qv2X0QTLK2ANu"
    RECAPTCHA_PRIVATE_KEY = "6Leg2OkUAAAAAJkKR0CIhMxxIS5eu65_dZYZW4oF"

    # Init database
    SQLALCHEMY_DATABASE_URI = 'postgres://wgfebwadpolfvi:61a91a8bd3230cc9ab9a020ba3517faeb998eedbe87723' \
                              '7c112d29114ff8736f@ec2-52-71-55-81.compute-1.amazonaws.com:5432' \
                              '/d2j2hkmdp0uifl'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
