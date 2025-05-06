
import { NextResponse } from 'next/server'

const PUBLIC_FILE = /\.(.*)$/



export async function middleware(req) {
  if (
    req.nextUrl.pathname.endsWith('/401') ||
    req.nextUrl.pathname.endsWith('/404') ||
    req.nextUrl.pathname.endsWith('/500') ||
    req.nextUrl.pathname.startsWith('/_next') ||
    PUBLIC_FILE.test(req.nextUrl.pathname)
  ) {
    return
  }
  let ok = false;
  try {
    let groups = [];
    const res = await fetch(`/api/o/v4/userinfo`);
    if ( res && res.status == 200 && res.data && res.data.groups ) 
      groups = res.data.groups;
    if ( groups && ( groups.indexOf('admin') !== -1 || user.groups.indexOf('datamanager') !== -1 )) 
      ok = true;
  }
  catch ( e ) {
    console.log(e);
  }  
  if ( ok )
    return NextResponse.redirect(new URL('/401', request.url));

  if (req.nextUrl.locale === 'default') {
    const locale = req.cookies.get('NEXT_LOCALE')?.value || 'en'
    return NextResponse.redirect(
      new URL(`/${locale}${req.nextUrl.pathname}${req.nextUrl.search}`, req.url)
    )
  }
}

