# LaudatorAI Deployment Guide

## 🚀 Phase 8: Deployment & Launch

This guide covers the complete deployment process for LaudatorAI, including staging and production environments.

## 📋 Prerequisites

### System Requirements
- Docker and Docker Compose installed
- At least 4GB RAM available
- 20GB free disk space
- Domain name (for production)
- SSL certificates (for production)

### Required Accounts
- OpenAI API key
- Domain registrar (for production)

## 🏗️ Environment Setup

### 1. Staging Environment

#### Step 1: Configure Environment Variables
```bash
# Copy the staging template
cp .env.staging.template .env.staging

# Edit the file with your actual values
nano .env.staging
```

#### Step 2: Deploy Staging
```bash
# Make deployment script executable
chmod +x scripts/deploy-staging.sh

# Run staging deployment
./scripts/deploy-staging.sh
```

#### Step 3: Verify Staging Deployment
- Frontend: http://localhost:3002
- Backend API: http://localhost:8001
- Grafana: http://localhost:3003
- Prometheus: http://localhost:9091
- MinIO Console: http://localhost:9003

### 2. Production Environment

#### Step 1: Configure Environment Variables
```bash
# Copy the production template
cp .env.production.template .env.production

# Edit the file with your actual values
nano .env.production
```

#### Step 2: SSL Certificate Setup
```bash
# Create SSL directory
mkdir -p nginx/ssl

# Place your SSL certificates
cp your-cert.pem nginx/ssl/cert.pem
cp your-key.pem nginx/ssl/key.pem
```

#### Step 3: Deploy Production
```bash
# Make deployment script executable
chmod +x scripts/deploy-production.sh

# Run production deployment
./scripts/deploy-production.sh
```

## 🔧 Configuration Details

### Environment Variables

#### Required Variables
- `POSTGRES_PASSWORD`: Secure database password
- `MINIO_ROOT_PASSWORD`: Secure MinIO password
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEXT_PUBLIC_API_URL`: Public API URL (for production)

#### Optional Variables
- `GRAFANA_PASSWORD`: Grafana admin password
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

### SSL Configuration

For production, you need valid SSL certificates:
- Certificate file: `nginx/ssl/cert.pem`
- Private key file: `nginx/ssl/key.pem`

You can obtain free certificates from Let's Encrypt or use your own certificates.

## 📊 Monitoring Setup

### Grafana Dashboard
1. Access Grafana at the configured URL
2. Login with admin/admin (or your custom password)
3. The LaudatorAI dashboard should be automatically provisioned
4. Key metrics to monitor:
   - API response times
   - Error rates
   - System resource usage
   - Database connections

### Prometheus Metrics
- Backend metrics: Available at `/metrics` endpoint
- System metrics: Collected via node-exporter
- Database metrics: PostgreSQL metrics
- Cache metrics: Redis metrics

## 🧪 Testing

### Load Testing
```bash
# Test staging environment
./scripts/load-test.sh staging http://localhost:8001

# Test production environment
./scripts/load-test.sh production https://your-domain.com
```

### Health Checks
```bash
# Check application health
curl -f http://localhost/health

# Check all services
docker-compose -f docker-compose.prod.yml ps
```

## 🔄 Rollback Procedures

### Quick Rollback
```bash
# Rollback production
./scripts/rollback.sh production

# Rollback staging
./scripts/rollback.sh staging
```

### Manual Rollback
1. Stop current deployment
2. Restore from backup
3. Restart services

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec postgres pg_isready

# Check logs
docker-compose -f docker-compose.prod.yml logs postgres
```

#### 2. SSL Certificate Issues
```bash
# Verify certificate files
ls -la nginx/ssl/

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

#### 3. Memory Issues
```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.prod.yml
```

#### 4. API Timeout Issues
```bash
# Check backend logs
docker-compose -f docker-compose.prod.yml logs backend

# Verify Redis connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

### Log Analysis
```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs backend
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Strong passwords for all services
- [ ] SSL certificates properly configured
- [ ] Firewall rules configured
- [ ] Regular security updates
- [ ] Database backups enabled
- [ ] Monitoring alerts configured

### Security Headers
The Nginx configuration includes security headers:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy
- Content-Security-Policy
- Strict-Transport-Security (HTTPS only)

## 📈 Performance Optimization

### Database Optimization
- Regular VACUUM operations
- Proper indexing
- Connection pooling

### Caching Strategy
- Redis for session storage
- Static file caching
- API response caching

### Load Balancing
- Nginx upstream configuration
- Health checks
- Rate limiting

## 🔄 Maintenance

### Regular Maintenance Tasks
1. **Daily**
   - Check application health
   - Monitor error rates
   - Review logs for issues

2. **Weekly**
   - Database maintenance
   - Log rotation
   - Security updates

3. **Monthly**
   - Performance review
   - Backup verification
   - SSL certificate renewal

### Backup Procedures
```bash
# Create database backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres laudatorai > backup_$(date +%Y%m%d).sql

# Backup MinIO data
docker-compose -f docker-compose.prod.yml exec minio mc mirror /data /backup
```

## 🎯 Launch Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Load testing completed
- [ ] Security audit performed
- [ ] Monitoring configured
- [ ] Backup procedures tested
- [ ] SSL certificates valid
- [ ] Domain DNS configured

### Launch Day
- [ ] Deploy to production
- [ ] Verify all services healthy
- [ ] Run smoke tests
- [ ] Monitor for issues
- [ ] Update DNS records
- [ ] Announce launch

### Post-Launch
- [ ] Monitor performance
- [ ] Gather user feedback
- [ ] Address any issues
- [ ] Plan future improvements

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify configuration files
4. Test in staging environment first

## 🔗 Useful Commands

```bash
# View service status
docker-compose -f docker-compose.prod.yml ps

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# View service logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Access service shell
docker-compose -f docker-compose.prod.yml exec backend bash

# Update and restart
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

This deployment guide ensures a smooth and secure launch of LaudatorAI in both staging and production environments.
