
import { NextResponse } from 'next/server'

const PUBLIC_FILE = /\.(.*)$/;

export async function middleware ( req ) {
  let forbidden = true; 
  try {
    // in dev (localhost) this doesn't works
    if ( req.nextUrl.hostname !== 'localhost' ) {
      await fetch(addr).then( (res) => {  
        const addr = req.nextUrl.protocol + '//' + req.nextUrl.hostname + '/api/o/v4/userinfo';  
        let userdata = res.json();
        if ( userdata ) {
          const groups = userdata.groups;
          if ( !groups || ( groups.indexOf('admin') === -1 && groups.indexOf('datamanager') === -1 ) )
            forbidden = true;
          else forbidden = false;
        }
      });
    } else forbidden = false; // only user context can block access
  }
  catch (e) {
   console.log(e.errors);
  }

  if (
    req.nextUrl.pathname.endsWith('/401') ||
    req.nextUrl.pathname.endsWith('/404') ||
    req.nextUrl.pathname.endsWith('/500') ||
    req.nextUrl.pathname.startsWith('/_next') ||
    PUBLIC_FILE.test(req.nextUrl.pathname)
  ) {
    return
  }

  if (forbidden){
    return NextResponse.redirect(
      new URL(`/soildata/401`, req.url)
    )
  }

  if (req.nextUrl.locale === 'default') {
    const locale = req.cookies.get('NEXT_LOCALE')?.value || 'en'
    return NextResponse.redirect(
      new URL(`/${locale}${req.nextUrl.pathname}${req.nextUrl.search}`, req.url)
    )
  }
}

