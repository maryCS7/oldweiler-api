# 🚀 Railway Production Deployment Instructions

## **For Business Reliability - Follow These Steps:**

### **1. Railway Account Setup**
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. **Upgrade to Railway Pro** ($5/month) for:
   - ✅ 99.9% uptime guarantee
   - ✅ No sleep/pause issues
   - ✅ Priority support
   - ✅ Better monitoring

### **2. Deploy the API**
1. **Create New Project** in Railway
2. **Connect GitHub Repository** (this repo)
3. **Add PostgreSQL Database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will auto-generate `DATABASE_URL`

### **3. Configure Environment Variables**
In Railway dashboard, go to your project → Variables tab:

```bash
# Database (Railway auto-provides this)
DATABASE_URL=postgresql://... (auto-generated)

# CORS
ALLOWED_ORIGINS=https://oldweilercustomcarpentry.com,https://www.oldweilercustomcarpentry.com

# Email (Resend)
RESEND_API_KEY=re_FovRaGJi_JKPqwXmQ6ty7kQQUDK5GjErc
FROM_EMAIL=info@oldweilercustomcarpentry.com
TO_EMAIL=OldweilerCustomCarpentry@gmail.com
COMPANY_NAME=Oldweiler Custom Carpentry
COMPANY_LOCATION=Bennington, NY

# Rate Limiting
RATE_LIMIT_REQUESTS=20
RATE_LIMIT_WINDOW=3600

# Environment
ENV=production
SKIP_EMAIL=false
```

### **4. Deploy Settings**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`

### **5. Test Production**
After deployment, test these URLs:
- `https://your-app-name.up.railway.app/health`
- `https://your-app-name.up.railway.app/docs`
- `https://your-app-name.up.railway.app/reviews/`

### **6. Update Frontend**
Update the frontend API URLs to point to your new Railway URL:
- `oldweiler-carpentry/src/app/contact/page.tsx`
- `oldweiler-carpentry/src/app/reviews/page.tsx`

## **Why This Setup is Business-Ready:**

✅ **Reliability**: Railway Pro ensures 99.9% uptime  
✅ **Monitoring**: Built-in health checks and logs  
✅ **Scalability**: Easy to upgrade as business grows  
✅ **Security**: Environment variables properly secured  
✅ **Backup**: PostgreSQL database with automatic backups  
✅ **Support**: Priority support for business issues  

## **Cost Breakdown:**
- **Railway Pro**: $5/month
- **PostgreSQL**: Included
- **Total**: $5/month for reliable business hosting

## **Monitoring Your Business Site:**
- Railway dashboard shows real-time status
- Health check endpoint for monitoring
- Email logs for contact form submissions
- Database logs for review submissions


