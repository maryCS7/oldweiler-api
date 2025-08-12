# 🚀 Oldweiler Custom Carpentry API - Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ **Backend API (oldweiler-api/)**
- [ ] **Database**: Set up PostgreSQL database (keep SQLite for simple deployments)
- [ ] **Environment Variables**: `.env` - fill in production values
- [ ] **Email Service**: Get Resend API key from https://resend.com
- [ ] **CORS**: Update `ALLOWED_ORIGINS` frontend domain
- [ ] **Environment**: Set `ENV=production`

### ✅ **Frontend (oldweiler-carpentry/)**
- [ ] **Build**: Run `npm run build` to create production build
- [ ] **Environment**: Set `NEXT_PUBLIC_API_BASE_URL` to your backend URL
- [ ] **Deploy**: Upload to hosting platform (Vercel, Netlify, etc.)

## 🌐 **Deployment Options**

### **Option 1: Simple Hosting (Recommended for Start)**
- **Backend**: Railway, Render, or Heroku
- **Frontend**: Vercel or Netlify
- **Database**: PostgreSQL add-on from hosting platform

### **Option 2: VPS/Cloud (More Control)**
- **Backend**: DigitalOcean, AWS, or Google Cloud
- **Frontend**: Same VPS or CDN
- **Database**: Managed PostgreSQL service

## 🔧 **Environment Variables for Production**

```bash
# Required
DATABASE_URL=postgresql://username:password@host:port/database_name
RESEND_API_KEY=your_resend_api_key_here
ENV=production

# Frontend domains (comma-separated)
ALLOWED_ORIGINS=https://yoursite.com,https://www.yoursite.com

# Optional: Customize
FROM_EMAIL=info@yoursite.com
TO_EMAIL=your-email@example.com
COMPANY_NAME=Your Company Name
COMPANY_LOCATION=Your Location
```

## 📊 **Monitoring & Health Checks**

### **Built-in Monitoring**
- **API Docs**: `https://your-api.com/docs`
- **Health Check**: `https://your-api.com/health`
- **OpenAPI**: `https://your-api.com/openapi.json`

### **What to Monitor**
- [ ] **Health endpoint** returns "healthy" status
- [ ] **Database connectivity** is working
- [ ] **Email service** can send messages
- [ ] **Rate limiting** is protecting against spam

## 🚨 **Post-Deployment Testing**

### **Test These Endpoints**
1. **`GET /`** - Welcome message
2. **`GET /health`** - Health check
3. **`GET /reviews/`** - Get reviews
4. **`POST /contact/`** - Submit contact form
5. **`GET /docs`** - API documentation

### **Common Issues & Solutions**
- **CORS errors**: Check `ALLOWED_ORIGINS` includes your frontend domain
- **Database errors**: Verify `DATABASE_URL` is correct
- **Email failures**: Check `RESEND_API_KEY` is valid
- **Rate limiting**: Test with multiple rapid requests

## 🎯 **Ready to Deploy!**

Your API is now **production-ready** with:
- ✅ Environment-based configuration
- ✅ Production database support
- ✅ CORS security
- ✅ Email service integration
- ✅ Rate limiting protection
- ✅ Input validation
- ✅ Health monitoring
- ✅ Comprehensive logging

**Next step**: Choose your hosting platform and follow their deployment instructions!
