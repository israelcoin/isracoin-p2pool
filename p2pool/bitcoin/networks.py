import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    bitcoin=math.Object(
        P2P_PREFIX='f9beb4d9'.decode('hex'),
        P2P_PORT=8333,
        ADDRESS_VERSION=0,
        RPC_PORT=8332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            (yield check_genesis_block(bitcoind, '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='BTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bitcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bitcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://blockchain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://blockchain.info/address/',
        TX_EXPLORER_URL_PREFIX='https://blockchain.info/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    bitcoin_testnet=math.Object(
        P2P_PREFIX='0b110907'.decode('hex'),
        P2P_PORT=18333,
        ADDRESS_VERSION=111,
        RPC_PORT=18332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bitcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='tBTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bitcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bitcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/address/',
        TX_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),

    namecoin=math.Object(
        P2P_PREFIX='f9beb4fe'.decode('hex'),
        P2P_PORT=8334,
        ADDRESS_VERSION=52,
        RPC_PORT=8332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'namecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='NMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Namecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Namecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.namecoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.dot-bit.org/b/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.dot-bit.org/a/',
        TX_EXPLORER_URL_PREFIX='http://explorer.dot-bit.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.2e8,
    ),
    namecoin_testnet=math.Object(
        P2P_PREFIX='fabfb5fe'.decode('hex'),
        P2P_PORT=18334,
        ADDRESS_VERSION=111,
        RPC_PORT=8332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'namecoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='tNMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Namecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Namecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.namecoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://testnet.explorer.dot-bit.org/b/',
        ADDRESS_EXPLORER_URL_PREFIX='http://testnet.explorer.dot-bit.org/a/',
        TX_EXPLORER_URL_PREFIX='http://testnet.explorer.dot-bit.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),

    litecoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9333,
        ADDRESS_VERSION=48,
        RPC_PORT=9332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'litecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='LTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Litecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Litecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.litecoin'), 'litecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/address/',
	      TX_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    litecoin_testnet=math.Object(
        P2P_PREFIX='fcc1b7dc'.decode('hex'),
        P2P_PORT=19333,
        ADDRESS_VERSION=111,
        RPC_PORT=19332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'litecoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='tLTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Litecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Litecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.litecoin'), 'litecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://nonexistent-litecoin-testnet-explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://nonexistent-litecoin-testnet-explorer/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),

    terracoin=math.Object(
        P2P_PREFIX='42babe56'.decode('hex'),
        P2P_PORT=13333,
        ADDRESS_VERSION=0,
        RPC_PORT=13332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'terracoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 20*100000000 >> (height + 1)//1050000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=120, # s
        SYMBOL='TRC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Terracoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Terracoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.terracoin'), 'terracoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://cryptocoinexplorer.com:3750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://cryptocoinexplorer.com:3750/address/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    terracoin_testnet=math.Object(
        P2P_PREFIX='41babe56'.decode('hex'),
        P2P_PORT=23333,
        ADDRESS_VERSION=111,
        RPC_PORT=23332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'terracoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 20*100000000 >> (height + 1)//1050000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=120, # s
        SYMBOL='tTRC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Terracoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Terracoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.terracoin'), 'terracoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://cryptocoinexplorer.com:3750/testnet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://cryptocoinexplorer.com:3750/testnet/address/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),

    digitalcoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=7999,
        ADDRESS_VERSION=30,
        RPC_PORT=7998,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'digitalcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 15*1000000000 >> (height + 1)//4730400,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s targetspacing
        SYMBOL='DGC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'digitalcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/digitalcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.digitalcoin'), 'digitalcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://altcha.in/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://altcha.in/address/',
	      TX_EXPLORER_URL_PREFIX='http://altcha.in/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    
    worldcoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=11081,
        ADDRESS_VERSION=73,
        RPC_PORT=11082,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'worldcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 64*1000000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='WDC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'worldcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/worldcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.worldcoin'), 'worldcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/address/',
	      TX_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    
    craftcoin=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=12124,
        ADDRESS_VERSION=57,
        RPC_PORT=12123,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'craftcoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=300, # s targetspacing
        SYMBOL='CRC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'craftcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/craftcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.craftcoin'), 'craftcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/address/',
	      TX_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),

    casinocoin=math.Object(
        P2P_PREFIX='fac3b6da'.decode('hex'),
        P2P_PORT=47950,
        ADDRESS_VERSION=28,
        RPC_PORT=47970,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'casinocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//3153600,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='CSC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'casinocoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/casinocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.casinocoin'), 'casinocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/address/',
	      TX_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/tx/',
	      SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    anoncoin=math.Object(
        P2P_PREFIX='facabada'.decode('hex'),
        P2P_PORT=9377,
        ADDRESS_VERSION=23,
        RPC_PORT=7332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'anoncoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 5*100000000 >> (height + 1)//306600,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=180, # s targetspacing
        SYMBOL='ANC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'anoncoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/anoncoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.anoncoin'), 'anoncoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.anoncoin.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.anoncoin.net/address/',
	      TX_EXPLORER_URL_PREFIX='http://explorer.anoncoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    bbqcoin=math.Object(
        P2P_PREFIX='fde4d942'.decode('hex'),
        P2P_PORT=19323,
        ADDRESS_VERSION=85,
        RPC_PORT=59332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bbqcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 42*100000000 >> (height + 1)//24000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='BQC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BBQCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BBQCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bbqcoin'), 'bbqcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bbq.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bbq.cryptocoinexplorer.com/address/',
	      TX_EXPLORER_URL_PREFIX='http://bbq.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
	      DUST_THRESHOLD=1e8,
    ),
    franko=math.Object(
        P2P_PREFIX='7defaced'.decode('hex'),
        P2P_PORT=7912,
        ADDRESS_VERSION=35,
        RPC_PORT=7913,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'frankoaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1*100000000 >> (height + 1)//1080000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='FRK',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'franko') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/franko/') if platform.system() == 'Darwin' else os.path.expanduser('~/.franko'), 'franko.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://d.evco.in/abe/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://d.evco.in/abe/address/',
	      TX_EXPLORER_URL_PREFIX='http://d.evco.in/abe/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
	      DUST_THRESHOLD=1e8,
    ),
    dogecoin=math.Object(
        P2P_PREFIX='c0c0c0c0'.decode('hex'),
        P2P_PORT=22556,
        ADDRESS_VERSION=30,
        RPC_PORT=22555,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'dogecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='DOGE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'DogeCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dogecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dogecoin'), 'dogecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://dogechain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://dogechain.info/address/',
        TX_EXPLORER_URL_PREFIX='http://dogechain.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    potcoin=math.Object(
            P2P_PREFIX='fbc0b6db'.decode('hex'),
            P2P_PORT=4200,
            ADDRESS_VERSION=55,
            RPC_PORT=42000,
            RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
                'potcoinaddress' in (yield bitcoind.rpc_help()) and
                not (yield bitcoind.rpc_getinfo())['testnet']
            )),
            SUBSIDY_FUNC=lambda height: 420*100000000 >> (height + 1)//840000,
            POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
            BLOCK_PERIOD=40, # s
            SYMBOL='POT',
            CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'potcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/potcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.potcoin'), 'potcoin.conf'),
            BLOCK_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/block/',
            ADDRESS_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/address/',
            TX_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/tx/',
            SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
            DUMB_SCRYPT_DIFF=2**16,
       	    DUST_THRESHOLD=0.03e8,
        ),
    mooncoin=math.Object(
        P2P_PREFIX='f9f7c0e8'.decode('hex'),
        P2P_PORT=44664,
        ADDRESS_VERSION=3,
        RPC_PORT=44663,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'tomooncoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2000000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=90, # s
        SYMBOL='MOON',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'MoonCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Mooncoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.mooncoin'), 'mooncoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://moonchain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://moonchain.info/address/',
        TX_EXPLORER_URL_PREFIX='http://moonchain.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    globalcoin=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=55789,
        ADDRESS_VERSION=15,
        RPC_PORT=55788,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'globalcoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 100*100000000 >> (height + 1)//288400,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s targetspacing
        SYMBOL='GLC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'globalcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/globalcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.globalcoin'), 'globalcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blockchainx.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blockchainx.com/address/',
	      TX_EXPLORER_URL_PREFIX='http://blockchainx.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    feathercoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9336,
        ADDRESS_VERSION=14,
        RPC_PORT=9337,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'feathercoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 200*100000000 >> (height + 1)//3360000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='FTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Feathercoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Feathercoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.feathercoin'), 'feathercoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.feathercoin.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.feathercoin.com/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.feathercoin.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    leafcoin=math.Object(
        P2P_PREFIX='aaaaaacc'.decode('hex'), #pchmessagestart
        P2P_PORT=22814,
        ADDRESS_VERSION=95, #pubkey_address
        RPC_PORT=22812,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'leafcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 100000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='LEAF',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'LeafCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Leafcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.leafcoin'), 'leafcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.leafco.in/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.leafco.in/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.leafco.in/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    smartcoin=math.Object(
        P2P_PREFIX='defaced0'.decode('hex'), #pchmessagestart
        P2P_PORT=58585,
        ADDRESS_VERSION=63, #pubkey_address
        RPC_PORT=58583,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'smartcoin' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 64*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s
        SYMBOL='SMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'smartcoin')
if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/smartcoin/')
if platform.system() == 'Darwin' else os.path.expanduser('~/.smartcoin'), 'smartcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='http://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0,
    ),
digibyte=math.Object(
        P2P_PREFIX='fac3b6da'.decode('hex'), #pchmessagestart
        P2P_PORT=12024,
        ADDRESS_VERSION=30, #pubkey_address
        RPC_PORT=14022,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'digibyteaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 8000*100000000 >> (height + 1)//1051200,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='DGB',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'digibyte') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/digibyte/') if platform.system() == 'Darwin' else os.path.expanduser('~/.digibyte'), 'digibyte.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='http://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.0001,
    ),
    flappycoin=math.Object(
        P2P_PREFIX='c1c1c1c1'.decode('hex'),
        P2P_PORT=11556,
        ADDRESS_VERSION=35,
        RPC_PORT=11555,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'flappycoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60,
        SYMBOL='FLAP',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'FlappyCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Flappycoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.flappycoin'), 'flappycoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://flapplorer.flappycoin.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://flapplorer.flappycoin.info/address/',
        TX_EXPLORER_URL_PREFIX='http://flapplorer.flappycoin.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    kittehcoin=math.Object(
        P2P_PREFIX='c0c0c0c0'.decode('hex'), #pchmessagestart
        P2P_PORT=22566,
        ADDRESS_VERSION=45, #pubkey_address
        RPC_PORT=22565,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'kittehcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='MEOW',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'kittehcoin')
if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/kittehcoin/')
if platform.system() == 'Darwin' else os.path.expanduser('~/.kittehcoin'), 'kittehcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://kitexplorer.tk/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://kitexplorer.tk/address/',
        TX_EXPLORER_URL_PREFIX='http://kitexplorer.tk/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.000001,
    ),
   nyancoin=math.Object(
       P2P_PREFIX='fcd9b7dd'.decode('hex'),
       P2P_PORT=33701,
       ADDRESS_VERSION=45,
       RPC_PORT=33700,
       RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
           'nyancoin address' in (yield bitcoind.rpc_help()) and
           not (yield bitcoind.rpc_getinfo())['testnet']
       )),
       SUBSIDY_FUNC=lambda height: 337*100000000 >> (height + 1)//500000,
       POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
       BLOCK_PERIOD=60, # s targetspacing
       SYMBOL='NYAN',
       CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'nyancoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/nyancoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.nyancoin'), 'nyancoin.conf'),
       BLOCK_EXPLORER_URL_PREFIX='http://nyancha.in/block/',
       ADDRESS_EXPLORER_URL_PREFIX='http://nyancha.in/address/',
       TX_EXPLORER_URL_PREFIX='http://nyancha.in/tx/',
       SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
       DUMB_SCRYPT_DIFF=2**16,
       DUST_THRESHOLD=1e8,
   ),
    mincoin=math.Object(
        P2P_PREFIX='6342212C'.decode('hex'),
        P2P_PORT=9772,
        ADDRESS_VERSION=50,
        RPC_PORT=9771,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'mincoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2*100000000 >> (height + 1)//105000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s targetspacing
        SYMBOL='MNC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Mincoin')
if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Mincoin/')
if platform.system() == 'Darwin' else os.path.expanduser('~/.mincoin'), 'mincoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://mnc.cryptoexplore.com/abe/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://mnc.cryptoexplore.com/abe/address/',
        TX_EXPLORER_URL_PREFIX='http://mnc.cryptoexplore.com/abe/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    megacoin=math.Object(
        P2P_PREFIX='ede0e4ee'.decode('hex'),
        P2P_PORT=7951,
        ADDRESS_VERSION=50,
        RPC_PORT=7950,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'megacoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='MEC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'megacoin')
if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Megacoin/')
if platform.system() == 'Darwin' else os.path.expanduser('~/.megacoin'), 'megacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://mega.rapta.net:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://mega.rapta.net:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://mega.rapta.net:2750/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
     aircoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=1631,
        ADDRESS_VERSION=23,
        RPC_PORT=1630,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'AIRcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='AIR',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'aircoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/aircoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.aircoin'), 'aircoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.teamaircoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.teamaircoin.org/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.teamaircoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
      ),
        plncoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9334,
        ADDRESS_VERSION=22,
        RPC_PORT=9331,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'plncoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 44*100000000 >> (height + 1)//438000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s targetspacing
        SYMBOL='PLN',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'plncoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/plncoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.plncoin'), 'plncoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.plnc.cryptor.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.plnc.cryptor.net/address/',
	      TX_EXPLORER_URL_PREFIX='http://explorer.plnc.cryptor.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
     pxlcoin=math.Object(
        P2P_PREFIX='d578c918'.decode('hex'),
        P2P_PORT=17765,
        ADDRESS_VERSION=0,
        RPC_PORT=17764,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'pxlcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 25*100000000 >> (height + 1)//200000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=420, # s
        SYMBOL='PXL',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'pxlcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/pxlcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.aircoin'), 'pxlcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blocks.pxlcoin.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blocks.pxlcoin.com/address/',
        TX_EXPLORER_URL_PREFIX='http://blocks.pxlcoin.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
      forexcoin=math.Object(
        P2P_PREFIX='fdc2b8dd'.decode('hex'),
        P2P_PORT=9369,
        ADDRESS_VERSION=35,
        RPC_PORT=9368,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'forexcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50000*100000000 >> (height + 1)//100000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='FRX',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'forexcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/forexcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.forexcoin'), 'aircoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://browser.globalforexcoin.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://browser.globalforexcoin.com/address/',
        TX_EXPLORER_URL_PREFIX='http://browser.globalforexcoin.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
      macrocoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=8306,
        ADDRESS_VERSION=20,
        RPC_PORT=8308,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'macrocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1*100000000 >> (height + 1)//2628000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='MCR',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'macrocoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/macrocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.macrocoin'), 'macrocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='https://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
      bitcoinscrypt=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=30201,
        ADDRESS_VERSION=0,
        RPC_PORT=30200,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bitcoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='BTCS',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'bitcoinscrypt') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/bitcoinscrypt/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoinscrypt'), 'aircoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blocks.btc2.pw/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blocks.btc2.pw//address/',
        TX_EXPLORER_URL_PREFIX='http://blocks.btc2.pw//tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
     egulden=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=11015,
        ADDRESS_VERSION=48,
        RPC_PORT=21015,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'litecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 25*100000000 >> (height + 1)//210000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='EFL',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'egulden') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/egulden/') if platform.system() == 'Darwin' else os.path.expanduser('~/.egulden'), 'egulden.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://altexplorer.net//address/',
        TX_EXPLORER_URL_PREFIX='https://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
    teslax3=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=1943,
        ADDRESS_VERSION=66,
        RPC_PORT=1856,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'teslax3address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 33*100000000 >> (height + 1)//210000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='TESLA',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'teslax3') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/teslax3/') if platform.system() == 'Darwin' else os.path.expanduser('~/.teslax3'), 'teslax3.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://altexplorer.net//address/',
        TX_EXPLORER_URL_PREFIX='https://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
greececoin=math.Object(
        P2P_PREFIX='d0c3deec'.decode('hex'),
        P2P_PORT=8541,
        ADDRESS_VERSION=38,
        RPC_PORT=8274,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'GreeceCoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 32*100000000 >> (height + 1)//250000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='GRCE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'teslax3') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/teslax3/') if platform.system() == 'Darwin' else os.path.expanduser('~/.teslax3'), 'teslax3.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='https://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
germanycoin=math.Object(
        P2P_PREFIX='fb149200'.decode('hex'),
        P2P_PORT=12267,
        ADDRESS_VERSION=38,
        RPC_PORT=12266,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'germanycoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 25*100000000 >> (height + 1)//250000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='GER',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'germanycoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/germanycoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.germanycoin'), 'germanycoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://188.226.223.81:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://188.226.223.81:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://188.226.223.81:2750/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
blitzcoin=math.Object(
        P2P_PREFIX='a9c5bdd1'.decode('hex'),
        P2P_PORT=24058,
        ADDRESS_VERSION=25,
        RPC_PORT=24056,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'Coinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='BLTZ',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'blitzcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/blitzcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.blitzcoin'), 'blitzcoin.conf'),
         BLOCK_EXPLORER_URL_PREFIX='http://cryptexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://cryptexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://cryptexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),
isracoin=math.Object(
        P2P_PREFIX='cfbdbe9c'.decode('hex'),
        P2P_PORT=21948,
        ADDRESS_VERSION=102,
        RPC_PORT=21947,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'isracoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//4773602,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='ISR',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'isracoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/isracoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.isracoin'), 'blitzcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bexplorer.israelcoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bexplorer.israelcoin.org/address/',
        TX_EXPLORER_URL_PREFIX='http://bexplorer.israelcoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
      ),


)
for net_name, net in nets.iteritems():
    net.NAME = net_name
