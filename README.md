# fax2tweet

Takes a PDF, converts the first page into a PNG and then tweets it. The intended use is converting faxes into Tweets with Asterisk.

It's an unpolished proof of concept. But should get you started.

# Requirements

You need python3, the modules in requirements.txt, and the libtiff-tools and poppler-utils packages.

You also need to create an "app" with a Twitter Developer account, give it read/write access in the oauth configuration, and then create the access and consumer keys.
I didn't document this part, sorry.

## Env Vars
Twitter API creds are supplied as env vars. They're self explanatory:

FAX2TWEET_CONSUMER_KEY
FAX2TWEET_CONSUMER_SECRET
FAX2TWEET_ACCESS_TOKEN
FAX2TWEET_ACCESS_TOKEN_SECRET

## Usage

fax2tweet.py [Path to TIFF] [Text to Tweet]

## Asterisk Config

    [recv-fax]
    exten => s,1,Noop("Connected to recv-fax")
    same => n,Answer()
    same => n,Set(TWEETTEXT=Fax from ${CALLERID(number)})
    same => n,Set(FAXDEST=/tmp/faxes)
    same => n,Set(FAXNAME=${STRFTIME(,,%C%y%m%d%H%M)})
    same => n,Set(FAXPATH=${FAXDEST}${FAXNAME})
    same => n,ReceiveFax(${FAXPATH}.tif)
    same => n,Noop(Converting tif to pdf)
    same => n,Set(TIFF2PDF=${SHELL(tiff2pdf ${FAXPATH}.tif -o ${FAXPATH}.pdf)})
    same => n,Noop(Sending Tweet)
    same => n,Noop(PDF Path: ${FAXPATH}.pdf)
    same => n,Set(FAX2TWEET=${SHELL(python3 -u /var/lib/asterisk/bin/fax2tweet.py ${FAXPATH}.pdf "${TWEETTEXT}" >> /tmp/log)})
    same => n,Noop(Deleting old file)
    same => n,Set(DELETE=${SHELL(rm ${FAXPATH}*)})
    same => n,Wait(30)
    same => n,Hangup()

# License

Released under the MIT license. See the LICENSE file.