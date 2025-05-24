class Config:
    """Base configuration."""
    # Add any configuration variables here
    pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False 