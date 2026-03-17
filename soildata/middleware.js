import { NextResponse } from 'next/server'

const PUBLIC_FILE = /\.(.*)$/;

export async function middleware ( req ) {
  

  if (
    req.nextUrl.pathname.endsWith('/401') ||
    req.nextUrl.pathname.endsWith('/404') ||
    req.nextUrl.pathname.endsWith('/500') ||
    req.nextUrl.pathname.startsWith('/_next') ||
    PUBLIC_FILE.test(req.nextUrl.pathname)
  ) {
    return
  }

  if (req.nextUrl.locale === 'default') {
    const locale = req.cookies.get('NEXT_LOCALE')?.value || 'en'
    return NextResponse.redirect(
      new URL(`/${locale}${req.nextUrl.pathname}${req.nextUrl.search}`, req.url)
    )
  }
}

