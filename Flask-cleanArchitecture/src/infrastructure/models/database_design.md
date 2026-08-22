Table Users {
  UserID int [pk, increment]
  UserName varchar(100) [unique, not null]
  PasswordHash varchar(255) [not null]
  FullName varchar(255) [not null]
  Email varchar(255) [unique, not null]
  Phone varchar(20) [unique]
  Avatar varchar(255)
  Gender varchar(255)
  CreatedAt datetime [not null]
  Status varchar(30) [not null]
  RoleID int [not null]
}

Table Roles {
  RoleID int [pk, increment]
  RoleName varchar(255) [unique, not null]
  CreatedAt datetime [not null]
  CreatedBy int [not null]
  UpdatedAt datetime [not null]
  UpdatedBy int [not null]
}

Table ServiceProviders {
  ProviderID int [pk, increment]
  UserID int [unique, not null]
  BusinessName varchar(255) [not null]
  TaxCode varchar(50) [unique]
  BusinessAddress varchar(500) [not null]
  LicenseUrl varchar(500) [not null]
  VerificationStatus varchar(20) [not null]
  ApprovedAt datetime
  Bank_Info varchar(500)
  CreatedAt datetime [not null]
}

Table Categories {
  CategoryID int [pk, increment]
  CategoryName varchar(100) [not null]
  Description varchar(255) [not null]
  CategoryType varchar(50) [not null]
  CreatedAt datetime [not null]
}

Table CreativeSpaces {
  SpaceID int [pk, increment]
  ProviderID int [not null]
  SpaceName varchar(255) [not null]
  CategoryID int [not null]
  Description text
  SizeSqm numeric(8,2)
  MaxCapacity int [not null]
  OperatingHours varchar(100) [not null]
  PricingModel varchar(30) [not null]
  BasePrice numeric(12,2) [not null]
  Status varchar(20) [not null]
  Address varchar(500) [not null]
  CreatedAt datetime [not null]
}

Table SpaceImages {
  SpaceImageID int [pk, increment]
  SpaceID int [not null]
  ImageUrl varchar(500) [not null]
  UploadedAt datetime [not null]
}

Table Amenities {
  AmenityID int [pk, increment]
  AmenitieName varchar(255) [unique, not null]
}

Table SpaceAmenities {
  SpaceAmenitiesID int [pk, increment]
  SpaceID int [not null]
  AmenityID int [not null]

  Indexes {
    (SpaceID, AmenityID) [unique]
  }
}

Table Equipment {
  EquipmentID int [pk, increment]
  ProviderID int [not null]
  SpaceID int
  CategoryID int [not null]
  EquipmentName varchar(255) [not null]
  Brand varchar(100)
  Condition varchar(30) [not null]
  RentalPrice numeric(12,2) [not null]
  Status varchar(20) [not null]
  PurchaseDate datetime [not null]
  CreatedAt datetime [not null]
}

Table Consumables {
  ConsumableID int [pk, increment]
  ProviderID int [not null]
  ConsumableName varchar(255) [not null]
  ConsumableType varchar(255) [not null]
  Unit varchar(20) [not null]
  StockQuantity numeric(10,2)
  UnitPrice numeric(12,2) [not null]
  ExpiryDate date [not null]
}

Table EquipmentMaintenanceLogs {
  MaintenanceLogID int [pk, increment]
  EquipmentID int [not null]
  MaintenanceDate date [not null]
  Description varchar(255)
  Cost numeric(12,2)
  PerformedBy varchar(255)
  NextScheduledDate date
  Status varchar(30) [not null]
}

Table Bookings {
  BookingID int [pk, increment]
  PhotographerID int [not null]
  SpaceID int [not null]
  PackageID int
  StartTime datetime [not null]
  EndTime datetime [not null]
  Status varchar(20) [not null]
  TotalPrice numeric(12,2) [not null]
  CreatedAt datetime [not null]
}

Table BookingEquipment {
  BookingEquipmentID int [pk, increment]
  BookingID int [not null]
  EquipmentID int [not null]
  Quantity int
  RentalPrice numeric(12,2) [not null]

  Indexes {
    (BookingID, EquipmentID) [unique]
  }
}

Table ServiceSessions {
  SessionID int [pk, increment]
  BookingID int [unique, not null]
  CheckInTime datetime
  CheckOutTime datetime
  CheckInMethod varchar(20)
  ActualDurationMinutes int
  Notes text
  Status varchar(20) [not null]
}

Table SessionEquipmentUsage {
  SEUsageID int [pk, increment]
  SessionID int [not null]
  EquipmentID int [not null]
  Quantity int [not null]
  Notes varchar(255)

  Indexes {
    (SessionID, EquipmentID) [unique]
  }
}

Table SessionConsumableUsage {
  SCUsageID int [pk, increment]
  SessionID int [not null]
  ConsumableID int [not null]
  QuantityUsed numeric(10,2) [not null]
  Cost numeric(12,2) [not null]
}

Table Invoices {
  InvoiceID int [pk, increment]
  SessionID int [unique, not null]
  InvoiceNumber varchar(50) [unique, not null]
  SubTotal numeric(12,2) [not null]
  DiscountAmount numeric(12,2)
  TaxAmount numeric(12,2)
  TotalAmount numeric(12,2) [not null]
  IssuedAt datetime [not null]
}

Table InvoiceDetail {
  InvoiceDetailID int [pk, increment]
  InvoiceID int [not null]
  Description text [not null]
  Quantity int [not null]
  UnitPrice numeric(12,2) [not null]
  LineTotal numeric(12,2) [not null]
}

Table Payments {
  PaymentID int [pk, increment]
  InvoiceID int [not null]
  PaymentMethod varchar(255) [not null]
  Amount numeric(12,2) [not null]
  Status varchar(20) [not null]
  PaidAt datetime [not null]
}

Table ServicePackages {
  PackageID int [pk, increment]
  ProviderID int [not null]
  PackageName varchar(255) [not null]
  Description text
  Price numeric(12,2) [not null]
  Status varchar(20) [not null]
  CreatedAt datetime [not null]
}

Table PackageDetails {
  PackageDetailID int [pk, increment]
  PackageID int [not null]
  ItemType varchar(255) [not null]
  ReferenceID int [not null]
  Quantity numeric(10,2) [not null]
}

Table Promotions {
  PromotionID int [pk, increment]
  ProviderID int [not null]
  PackageID int
  Code varchar(50) [not null]
  DiscountType varchar(20) [not null]
  DiscountValue numeric(12,2) [not null]
  StartDate datetime [not null]
  EndDate datetime [not null]
  UsageLimit int
  Status varchar(20) [not null]
}

Table Reviews {
  ReviewID int [pk, increment]
  PhotographerID int [not null]
  BookingID int [not null]
  TargetType varchar(20) [not null]
  TargetID int [not null]
  Rating int [not null]
  Comment text
  CreatedAt datetime [not null]
}

Table Posts {
  PostID int [pk, increment]
  AuthorID int [not null]
  Title varchar(255) [not null]
  Content text [not null]
  Category varchar(30) [not null]
  Status varchar(30) [not null]
  CreatedAt datetime [not null]
}

Table PostComments {
  CommentID int [pk, increment]
  PostID int [not null]
  UserID int [not null]
  Content text [not null]
  CreatedAt datetime [not null]
}

Table Workshops {
  WorkshopID int [pk, increment]
  ProviderID int [not null]
  Title varchar(255) [not null]
  Description text
  Location varchar(500) [not null]
  StartTime datetime [not null]
  EndTime datetime [not null]
  Capacity int [not null]
  Fee numeric(12,2) [not null]
  Status varchar(20) [not null]
  CreatedAt datetime [not null]
}

Table WorkshopRegistrations {
  WorkshopRegistrationID int [pk, increment]
  WorkshopID int [not null]
  UserID int [not null]
  RegisteredAt datetime [not null]
  Status varchar(20) [not null]

  Indexes {
    (WorkshopID, UserID) [unique]
  }
}

Table AIInteractionLogs {
  AIInteractionLogID int [pk, increment]
  UserID int [not null]
  InteractionType varchar(30) [not null]
  QueryText text
  ResponseText text
  CreatedAt datetime [not null]
}

Table AIConfigurations {
  AIConfigID int [pk, increment]
  ConfigKey varchar(100) [unique, not null]
  ConfigValue varchar(255) [not null]
  IsActive boolean [not null]
  UpdatedAt datetime [not null]
  UpdatedBy int [not null]
}

Table Notifications {
  NotificationID int [pk, increment]
  UserID int [not null]
  Title varchar(255) [not null]
  Content text [not null]
  Type varchar(30) [not null]
  IsRead boolean [not null]
  CreatedAt datetime [not null]
}

Table Complaints {
  ComplaintID int [pk, increment]
  UserID int [not null]
  BookingID int
  TargetType varchar(20) [not null]
  TargetID int [not null]
  Description text [not null]
  Status varchar(20) [not null]
  ResolvedAt datetime
}


// ==================== RELATIONSHIPS ====================

// User - Role
Ref: Users.RoleID > Roles.RoleID

// Service Provider - User
Ref: ServiceProviders.UserID - Users.UserID

// Creative Space
Ref: CreativeSpaces.ProviderID > ServiceProviders.ProviderID
Ref: CreativeSpaces.CategoryID > Categories.CategoryID

// Space Images
Ref: SpaceImages.SpaceID > CreativeSpaces.SpaceID

// Space Amenities
Ref: SpaceAmenities.SpaceID > CreativeSpaces.SpaceID
Ref: SpaceAmenities.AmenityID > Amenities.AmenityID

// Equipment
Ref: Equipment.ProviderID > ServiceProviders.ProviderID
Ref: Equipment.SpaceID > CreativeSpaces.SpaceID
Ref: Equipment.CategoryID > Categories.CategoryID

// Consumables
Ref: Consumables.ProviderID > ServiceProviders.ProviderID

// Equipment Maintenance
Ref: EquipmentMaintenanceLogs.EquipmentID > Equipment.EquipmentID

// Booking
Ref: Bookings.PhotographerID > Users.UserID
Ref: Bookings.SpaceID > CreativeSpaces.SpaceID
Ref: Bookings.PackageID > ServicePackages.PackageID

// Booking Equipment
Ref: BookingEquipment.BookingID > Bookings.BookingID
Ref: BookingEquipment.EquipmentID > Equipment.EquipmentID

// Service Session
Ref: ServiceSessions.BookingID - Bookings.BookingID

// Session Equipment
Ref: SessionEquipmentUsage.SessionID > ServiceSessions.SessionID
Ref: SessionEquipmentUsage.EquipmentID > Equipment.EquipmentID

// Session Consumables
Ref: SessionConsumableUsage.SessionID > ServiceSessions.SessionID
Ref: SessionConsumableUsage.ConsumableID > Consumables.ConsumableID

// Invoice
Ref: Invoices.SessionID - ServiceSessions.SessionID

// Invoice Details (fix)
Ref: InvoiceDetail.InvoiceID > Invoices.InvoiceID

// Payment (fix)
Ref: Payments.InvoiceID > Invoices.InvoiceID

// Service Packages
Ref: ServicePackages.ProviderID > ServiceProviders.ProviderID

// Package Details (fix)
Ref: PackageDetails.PackageID > ServicePackages.PackageID

// Promotions
Ref: Promotions.ProviderID > ServiceProviders.ProviderID
Ref: Promotions.PackageID > ServicePackages.PackageID

// Reviews
Ref: Reviews.PhotographerID > Users.UserID
Ref: Reviews.BookingID > Bookings.BookingID

// Posts
Ref: Posts.AuthorID > Users.UserID

// Post Comments
Ref: PostComments.PostID > Posts.PostID
Ref: PostComments.UserID > Users.UserID

// Workshops
Ref: Workshops.ProviderID > ServiceProviders.ProviderID

// Workshop Registrations
Ref: WorkshopRegistrations.WorkshopID > Workshops.WorkshopID
Ref: WorkshopRegistrations.UserID > Users.UserID

// AI
Ref: AIInteractionLogs.UserID > Users.UserID
Ref: AIConfigurations.UpdatedBy > Users.UserID

// Notifications 
Ref: Notifications.UserID > Users.UserID

// Complaints
Ref: Complaints.UserID > Users.UserID
Ref: Complaints.BookingID > Bookings.BookingID





