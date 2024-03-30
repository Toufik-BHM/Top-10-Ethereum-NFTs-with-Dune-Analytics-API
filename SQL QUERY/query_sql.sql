SELECT
    row_number() OVER (ORDER BY SUM(amount_usd) DESC) AS "#",
    CASE 
        WHEN nft_contract_address = 0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb THEN 'CryptoPunks'
        ELSE collection
    END AS collection,
    nft_contract_address,
    COUNT(*) AS sales, 
    SUM(amount_usd) AS usd_volume,
    SUM(amount_original) AS eth_volume, 
    MIN(amount_original) AS lowest_sale, 
    MAX(amount_original) AS high_sale
FROM 
    nft.trades 
WHERE 
    nft_contract_address NOT IN  (
                    0x942bc2d3e7a589fe5bd4a5c6ef9727dfd82f5c8a, -- Art Blocks 1 
                    0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270, -- Art Blocks 2
                    0x059edd72cd353df5106d2b9cc5ab83a52287ac3a,
                    0x99a9b7c1116f9ceeb1652de04d5969cce509b069, -- Art Blocks 3 
                    0x64780ce53f6e966e18a22af13a2f97369580ec11, -- Art Blocks Partners 
                    0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c, 
                    0x97A20815a061EaE224c4fdF3109731f73743db73, --  LVCIDIA// RESOURCES
                    0x431Dcee2e2c267F32Dc4349619000B6Cef1Ba932, -- Free Mint
                    0xF03f8ed5D0CC1d933dc3A91cD7F73Db4dD2B1366, -- Loose Balloons
                    0x76be3b62873462d2142405439777e971754e8e77, 
                    0x495f947276749ce646f68ac8c248420045cb7b5e,
                    0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85, -- ENS slows everything down 
                    0xD4307E0acD12CF46fD6cf93BC264f5D5D1598792, -- Base Spam 
                    0x728863d7E094aE5fFD91DCC365099666020d7a51, -- Nakamatos 
                    0x8c9b261Faef3b3C2e64ab5E58e04615F8c788099, -- MLB 
                    0xa342f5D851E866E18ff98F351f2c6637f4478dB5, -- Sandbox Assets 
                    0xfaaFDc07907ff5120a76b34b731b278c38d6043C, -- Enjin 
                    0xd07dc4262BCDbf85190C01c996b4C06a461d2430, -- Raraible ERC 1155 
                    0xB66a603f4cFe17e3D27B87a8BfCaD319856518B8, -- Raraible ERC 1155 2 
                    0xa604060890923ff400e8c6f5290461a83aedacec, -- OpenSea SharedStorefront MINTS 
                    0x495f947276749Ce646f68AC8c248420045cb7b5e -- OpenSea SharedStorefront 
    )
    AND block_time BETWEEN TIMESTAMP '{{Start_Date}}' AND TIMESTAMP '{{End_Date}}'
    AND currency_symbol IN ('ETH', 'WETH')
    AND unique_trade_id NOT IN (SELECT unique_trade_id FROM nft.wash_trades WHERE is_wash_trade = true)
    AND blockchain = 'ethereum'
GROUP BY
    CASE 
        WHEN nft_contract_address = 0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb THEN 'CryptoPunks'
        ELSE collection
    END,
    nft_contract_address
ORDER BY usd_volume DESC
LIMIT 10;