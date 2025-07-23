import { NextResponse } from 'next/server'

const PUBLIC_FILE = /\.(.*)$/;

export async function middleware ( req ) {
  /*try {
     in dev (localhost) this doesn't works
    //if ( req.nextUrl.hostname !== 'localhost' ) {
      const addr = req.nextUrl.protocol + '//' + req.nextUrl.hostname + '/api/o/v4/userinfo';  
      let res = await fetch(addr);  
      if ( res && res.status == 200 ) {
        let userdata = res.json();
        if ( userdata ) {
          const groups = userdata.groups;
          if ( !groups || ( groups.indexOf('admin') === -1 && groups.indexOf('datamanager') === -1 ) )
            forbidden = true;
          else forbidden = false;
        }
      });
      console.log("middleware");
      console.log(forbidden);
    //} else forbidden = false; // only user context can block access
  }
  catch (e) {
    console.log("middleware");
    console.log(e);
  }
  */
  console.log('Cookie Header:', req.headers.get('cookie'));
  console.log('All Headers:', Object.fromEntries(req.headers));

  if (
    req.nextUrl.pathname.endsWith('/401') ||
    req.nextUrl.pathname.endsWith('/404') ||
    req.nextUrl.pathname.endsWith('/500') ||
    req.nextUrl.pathname.startsWith('/_next') ||
    PUBLIC_FILE.test(req.nextUrl.pathname)
  ) {
    return
  }

  /*
  if (forbidden){
    return NextResponse.redirect(
      new URL(`/soildata/401`, req.url)
    )
  } */

  if (req.nextUrl.locale === 'default') {
    const locale = req.cookies.get('NEXT_LOCALE')?.value || 'en'
    return NextResponse.redirect(
      new URL(`/${locale}${req.nextUrl.pathname}${req.nextUrl.search}`, req.url)
    )
  }
}

