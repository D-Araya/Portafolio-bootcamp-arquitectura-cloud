# Infraestructura como Código (IaC) - Terraform

## 📋 Configuración de AWS con Terraform

Este directorio contiene ejemplos de código Terraform para provisionar la infraestructura del proyecto "Nube Sólida" en AWS.

---

## 🗂️ Estructura de Archivos

```
terraform/
├── main.tf                 # Configuración principal
├── variables.tf            # Variables de entrada
├── outputs.tf              # Outputs de terraform
├── provider.tf             # Configuración del provider AWS
├── vpc.tf                  # Configuración de VPC y redes
├── ecs.tf                  # Configuración de ECS Fargate
├── rds.tf                  # Configuración de RDS
├── s3.tf                   # Configuración de S3
├── lambda.tf               # Configuración de Lambda
└── README.md               # Este archivo
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

1. **Instalar Terraform**
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
   unzip terraform_1.7.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   
   # Verificar instalación
   terraform --version
   ```

2. **Configurar AWS CLI**
   ```bash
   # Instalar AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   
   # Configurar credenciales
   aws configure
   # AWS Access Key ID: tu-access-key
   # AWS Secret Access Key: tu-secret-key
   # Default region: us-east-1
   # Default output format: json
   ```

### Despliegue

```bash
# 1. Inicializar Terraform
terraform init

# 2. Ver plan de ejecución
terraform plan

# 3. Aplicar cambios
terraform apply

# 4. Para destruir infraestructura (¡CUIDADO!)
terraform destroy
```

---

## 📝 Ejemplo: `main.tf`

```hcl
# main.tf - Configuración principal de la infraestructura

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Backend para almacenar el state en S3 (recomendado para producción)
  backend "s3" {
    bucket         = "nube-solida-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "Nube Sólida"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "DevOps Team"
    }
  }
}
```

---

## 📝 Ejemplo: `variables.tf`

```hcl
# variables.tf - Variables de entrada

variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
  default     = "prod"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "El ambiente debe ser dev, staging o prod."
  }
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "nube-solida"
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability Zones a usar"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "db_instance_class" {
  description = "Tipo de instancia para RDS"
  type        = string
  default     = "db.t3.medium"
}

variable "db_username" {
  description = "Username para la base de datos"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Password para la base de datos"
  type        = string
  sensitive   = true
}
```

---

## 📝 Ejemplo: `vpc.tf`

```hcl
# vpc.tf - Configuración de VPC y redes

# VPC Principal
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Subnets Públicas
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-${var.availability_zones[count.index]}"
    Type = "Public"
  }
}

# Subnets Privadas
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index + 10)
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.project_name}-private-${var.availability_zones[count.index]}"
    Type = "Private"
  }
}

# NAT Gateways (uno por AZ para alta disponibilidad)
resource "aws_eip" "nat" {
  count  = length(var.availability_zones)
  domain = "vpc"
  
  tags = {
    Name = "${var.project_name}-nat-eip-${var.availability_zones[count.index]}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = length(var.availability_zones)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${var.project_name}-nat-${var.availability_zones[count.index]}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = {
    Name = "${var.project_name}-private-rt-${var.availability_zones[count.index]}"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
```

---

## 📝 Ejemplo: `rds.tf`

```hcl
# rds.tf - Configuración de RDS PostgreSQL Multi-AZ

# Security Group para RDS
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group para RDS PostgreSQL"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "PostgreSQL desde ECS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# Subnet Group para RDS
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  
  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# RDS PostgreSQL Multi-AZ
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-postgres"
  engine         = "postgres"
  engine_version = "15.4"
  
  instance_class    = var.db_instance_class
  allocated_storage = 50
  storage_type      = "gp3"
  storage_encrypted = true
  
  # Multi-AZ para alta disponibilidad
  multi_az = true
  
  db_name  = "nubesolida"
  username = var.db_username
  password = var.db_password
  
  # Networking
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  
  # Backup
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"
  
  # Monitoring
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  monitoring_interval             = 60
  monitoring_role_arn             = aws_iam_role.rds_monitoring.arn
  
  # Performance Insights
  performance_insights_enabled = true
  
  # Configuraciones adicionales
  skip_final_snapshot       = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  deletion_protection       = true
  
  tags = {
    Name = "${var.project_name}-postgres"
  }
}

# IAM Role para RDS Enhanced Monitoring
resource "aws_iam_role" "rds_monitoring" {
  name = "${var.project_name}-rds-monitoring-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}
```

---

## 📝 Ejemplo: `outputs.tf`

```hcl
# outputs.tf - Outputs de Terraform

output "vpc_id" {
  description = "ID de la VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs de las subnets públicas"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs de las subnets privadas"
  value       = aws_subnet.private[*].id
}

output "rds_endpoint" {
  description = "Endpoint de la base de datos RDS"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "rds_database_name" {
  description = "Nombre de la base de datos"
  value       = aws_db_instance.main.db_name
}

output "alb_dns_name" {
  description = "DNS name del Application Load Balancer"
  value       = aws_lb.main.dns_name
}
```

---

## 🔐 Seguridad

### Gestión de Secretos

**NUNCA** commitees credenciales en el código. Usa:

1. **Terraform Variables con archivos `.tfvars`**
   ```bash
   # Crear archivo terraform.tfvars (añadir a .gitignore)
   db_username = "admin"
   db_password = "super-secret-password"
   ```

2. **AWS Secrets Manager**
   ```hcl
   data "aws_secretsmanager_secret_version" "db_password" {
     secret_id = "nube-solida/db-password"
   }
   
   resource "aws_db_instance" "main" {
     password = data.aws_secretsmanager_secret_version.db_password.secret_string
   }
   ```

3. **Variables de entorno**
   ```bash
   export TF_VAR_db_username="admin"
   export TF_VAR_db_password="super-secret"
   ```

---

## 🎯 Buenas Prácticas

1. **State Remoto**
   - Siempre usa S3 backend para state en equipo
   - Habilita versionado en S3
   - Usa DynamoDB para state locking

2. **Modularización**
   - Divide la infraestructura en módulos reutilizables
   - Un módulo por componente principal (VPC, ECS, RDS)

3. **Variables**
   - Usa variables para todos los valores configurables
   - Documenta cada variable con `description`
   - Usa `validation` blocks para validar inputs

4. **Tags**
   - Usa `default_tags` en el provider
   - Etiqueta TODOS los recursos
   - Incluye: Project, Environment, Owner, Cost Center

5. **Seguridad**
   - Nunca expongas secretos
   - Usa `sensitive = true` para variables sensibles
   - Implementa least privilege en IAM

---

## 📚 Recursos Adicionales

- [Documentación Oficial de Terraform](https://www.terraform.io/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

## 🆘 Troubleshooting

### Error: `Backend initialization required`
```bash
# Solución: Inicializar backend
terraform init
```

### Error: `Credentials not found`
```bash
# Solución: Configurar AWS CLI
aws configure
```

### Error: `Resource already exists`
```bash
# Solución: Importar recurso existente
terraform import aws_vpc.main vpc-xxxxxx
```

---

<div align="center">

**Infraestructura como Código = Infraestructura Reproducible y Versionada**

</div>
