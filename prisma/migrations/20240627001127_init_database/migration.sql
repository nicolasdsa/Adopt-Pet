-- CreateTable
CREATE TABLE "AdoptionLocation" (
    "id" STRING NOT NULL,
    "name" STRING NOT NULL,
    "description" STRING NOT NULL,
    "latitude" FLOAT8 NOT NULL,
    "longitude" FLOAT8 NOT NULL,
    "address" STRING NOT NULL,
    "locationTypeId" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AdoptionLocation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "LocationType" (
    "id" STRING NOT NULL,
    "name" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LocationType_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Animal" (
    "id" INT8 NOT NULL DEFAULT unique_rowid(),
    "name" STRING NOT NULL,
    "size" STRING NOT NULL,
    "age" INT4 NOT NULL,
    "animalTypeId" STRING NOT NULL,
    "needsMedicalHelp" BOOL NOT NULL,
    "description" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "adoptionLocationId" STRING NOT NULL,

    CONSTRAINT "Animal_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AnimalType" (
    "id" STRING NOT NULL,
    "name" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AnimalType_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Contact" (
    "id" STRING NOT NULL,
    "phone" STRING,
    "email" STRING,
    "instagram" STRING,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "adoptionLocationId" STRING NOT NULL,

    CONSTRAINT "Contact_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Donation" (
    "id" STRING NOT NULL,
    "pixKey" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "adoptionLocationId" STRING NOT NULL,

    CONSTRAINT "Donation_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "AdoptionLocation" ADD CONSTRAINT "AdoptionLocation_locationTypeId_fkey" FOREIGN KEY ("locationTypeId") REFERENCES "LocationType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Animal" ADD CONSTRAINT "Animal_animalTypeId_fkey" FOREIGN KEY ("animalTypeId") REFERENCES "AnimalType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Animal" ADD CONSTRAINT "Animal_adoptionLocationId_fkey" FOREIGN KEY ("adoptionLocationId") REFERENCES "AdoptionLocation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Contact" ADD CONSTRAINT "Contact_adoptionLocationId_fkey" FOREIGN KEY ("adoptionLocationId") REFERENCES "AdoptionLocation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Donation" ADD CONSTRAINT "Donation_adoptionLocationId_fkey" FOREIGN KEY ("adoptionLocationId") REFERENCES "AdoptionLocation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
