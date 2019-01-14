[['进入ADSCoin'], ['认 购','采 矿'], ['中文汉化', '翻 墙'],['邀请朋友','English/中文']]
[['Enter ADSCoin'], ['Purchase','Mining'], ['Chinese Localization', 'VPN Tunnelling'],['Invite Friends','English/中文']]

 keyboard = [[InlineKeyboardButton("进入ADSCoin认购", url='http://www.adscoin.shop/wallet/buysell/')]]
 "Enter ADSCoin to buy"

            update.message.reply_text('ADSCoin官方站点!', reply_markup=reply_markup, )
			'ADSCoin Official Website'

        if update.message.text == '进入ADSCoin':
		'Enter ADSCoin'

        if update.message.text == '采 矿':
		'Mining'
            keyboard = [[InlineKeyboardButton("进入采矿任务", url='http://www.adscoin.shop/mining.html')]]
			'Enter for mining task'
            update.message.reply_text('ADSCoin采矿', reply_markup=reply_markup, )
			'ADSCoin Mining'

        if update.message.text == 'English/中文':

        if update.message.text == '中文汉化':
		'Chinese Localization'
		  caption='Android(安卓手机)\n使用方法: 点击上方蓝色的“↓”按钮下载，完成之后点击消息上的三个小灰点，选择 Apply localization file (使用本地化文件)',
			'Android\nUsage: Click the blue “↓” button to download. After that, click the little grey dot above the message, select Apply localization file (使用本地化文件)',
		  caption='Windows,Linux,macOS\n使用方法:进入Settings(设置)，键盘上按住Alt+Shift，然后点击"Change Language（更改语言）"\n\n在macOS环境下安装翻译时，请确保语言文件存放在Download文件夹。',
			'Windows,Linux,macOS\nUsage: Enter Settings, press Alt+Shift on the keyboard, then click "Change Language"\n\nWhen installing localization on macOS, please ensure that the language pack is contained in the Download folder.'
		  caption='苹果手机(IOS)\n使用方法: 点击上方蓝色的“↓”按钮下载，下载之后点击文件，选择 Apply localization (使用本地化)\n应用后有“可能会出现错误提示”，请点击 OK 忽略',
			'iphone(iOS)\nUsage: Click the blue “↓” button to download. After that, click on the downloaded file, select Apply localization\nAfter applying the localization, you may receive an error message, please ignore it and click OK'

        if update.message.text == '翻 墙':
		'VPN Tunnelling'
		 text='<a href="https://t.me/proxy?server=jp.3412.ml&port=9981&secret=030c0046b23166a31321f563e9883b81">1号服务器\n点这里自动配置到您的Telegram</a>\n\n<a href="https://t.me/proxy?server=jp.telepro.cf&port=9981&secret=c70ecdabfb228573d81de2dbf53ac0e3">2号服务器\n点这里自动配置到您的Telegram</a>\n\n<b>Telegram专用翻墙工具,永久高速免费,上Telegram专用</b>',
		 text='<a href="https://t.me/proxy?server=jp.3412.ml&port=9981&secret=030c0046b23166a31321f563e9883b81">1号服务器\n点这里自动配置到您的Telegram</a>\n\n<a href="https://t.me/proxy?server=jp.telepro.cf&port=9981&secret=c70ecdabfb228573d81de2dbf53ac0e3">Server No 2\nClick here to automatically setup to your Telegram</a>\n\n<b>Exclusive tunnelling tool for VPN, high speed & FREE forever, optimized for Telegram</b>',

        if update.message.text == '邀请朋友':
		'Invite Friends'
		
update.message.reply_text('ADSCoin登入失败点这里再试一次 /start')
update.message.reply_text('ADSCoin Login error, please click here to retry /start')


update.message.reply_text('您可以把以下贴子分享给您的朋友,一起加入ASDCoin 成功邀请赠送ADS ↴')
update.message.reply_text('You may share the thread to your friends, and invite them to join ASDCoin. Every successful invitation will be given FREE ADS')

	
keyboard = [[InlineKeyboardButton("10秒内点击进入ADSCoin", url=websocketioippro + '/sign/%s/%s/' % (
"Enter ADSCoin within 10 seconds"

update.message.reply_text('登陆钱包,都由此进入!', reply_markup=reply_markup, )
'Login to your wallet, enter from here'
